#!/usr/bin/env python3
"""
Generate synthetic benchmark data for the PCS dashboard.

- Writes daily NDJSON files under bench/results/YYYY-MM-DD.ndjson
- Aggregates to site/benchmarks.json as a JSON array (what the dashboard expects)
- Reproducible via --seed (default 1337)

Usage:
  python scripts/generate_demo_data.py --days 7 --backends julia,rust,go,ts,csharp --out site/benchmarks.json
"""
import argparse
import datetime
import json
import math
import pathlib
import random
from typing import Dict, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "bench" / "results"
SITE_DIR = ROOT / "site"

DEFAULT_BACKENDS = ["julia", "rust", "go", "ts", "csharp"]
DEFAULT_TESTS = [
    # (name, base_ns at N=1e6)
    ("sum_even_squares", 1_600_000.0),
    ("groupby_topN", 3_200_000.0),
    ("time_buckets", 2_400_000.0),
]

# Backend multipliers (mean performance vs the default base)
BACKEND_MULT = {
    "julia": 0.95,
    "rust": 0.80,
    "go": 0.90,
    "ts": 1.40,
    "csharp": 1.00,
}

# Typical parallel speedups (lower is faster)
PAR_SPEEDUP = {
    "julia": 0.55,
    "rust": 0.45,
    "go": 0.60,
    "ts": 0.75,
    "csharp": 0.65,
}


def lognormal_noise(mu=0.0, sigma=0.08):
    # multiplicative noise ~ exp(N(mu, sigma^2))
    return math.exp(random.gauss(mu, sigma))


def synth_row(
    backend, test, base_ns, mode, parallel, n, commit, ts_iso, os_name, cpu
) -> Dict:
    # scale by backend
    ns = base_ns * BACKEND_MULT.get(backend, 1.0)

    # scale by N (approx linear)
    scale = n / 1_000_000
    ns *= scale

    # parallel mode → speedup factor
    if parallel:
        ns *= PAR_SPEEDUP.get(backend, 0.7)

    # per-mode tweak: broadcast a bit faster than loops for small-N map
    if mode == "broadcast" and test == "sum_even_squares" and n <= 200_000:
        ns *= 0.9

    # add realistic multiplicative noise
    mean_ns = ns * lognormal_noise()
    std_ns = mean_ns * 0.05

    return {
        "commit": commit,
        "timestamp": ts_iso,
        "os": os_name,
        "cpu": cpu,
        "backend": backend,
        "test": test,
        "mode": mode,
        "parallel": bool(parallel),
        "n": int(n),
        "mean_ns": float(mean_ns),
        "std_ns": float(std_ns),
        "reps": 5,
        "k_policy": "best-of-k",
        "generator": "pcs@demo",
        "bench_runner_ver": "1.0.0",
        "policy_sha": "demo-policy-sha",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of past days to synthesize (including today).",
    )
    ap.add_argument(
        "--seed", type=int, default=1337, help="RNG seed for reproducibility."
    )
    ap.add_argument("--backends", type=str, default=",".join(DEFAULT_BACKENDS))
    ap.add_argument(
        "--tests", type=str, default=",".join([t for t, _ in DEFAULT_TESTS])
    )
    ap.add_argument(
        "--n-list", type=str, default="100000,1000000", help="Comma-separated N sizes."
    )
    ap.add_argument("--out", type=str, default=str(SITE_DIR / "benchmarks.json"))
    ap.add_argument("--os", type=str, default="ubuntu-22.04")
    ap.add_argument("--cpu", type=str, default="GitHub Actions (vCPU)")
    args = ap.parse_args()

    random.seed(args.seed)
    backends = [b.strip() for b in args.backends.split(",") if b.strip()]
    n_list = [int(x) for x in args.n_list.split(",") if x.strip()]
    test_map = {}
    for pair in args.tests.split(","):
        name = pair.strip()
        default = dict(DEFAULT_TESTS)
        base = default.get(name, 1_800_000.0)
        test_map[name] = base

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    SITE_DIR.mkdir(parents=True, exist_ok=True)

    all_rows: List[Dict] = []

    # Generate from oldest to today
    today = datetime.datetime.utcnow().date()
    for delta in range(args.days - 1, -1, -1):
        day = today - datetime.timedelta(days=delta)
        ts_base = datetime.datetime.combine(
            day, datetime.time(7, 0), tzinfo=datetime.timezone.utc
        )
        ndjson_path = RESULTS_DIR / f"{day.isoformat()}.ndjson"
        rows: List[Dict] = []

        for backend in backends:
            for test, base_ns in test_map.items():
                for n in n_list:
                    # modes: loops, broadcast (for sum_even_squares small N), parallel loops
                    for mode, parallel in [
                        ("loops", False),
                        ("broadcast", False),
                        ("loops", True),
                    ]:
                        # make sure broadcast shows only for small-N map test (optional prettiness)
                        if mode == "broadcast" and (
                            test != "sum_even_squares" or n > 200_000
                        ):
                            continue
                        commit = f"demo-{day.strftime('%m%d')}-{backend[:2]}{random.randint(100,999)}"
                        ts_iso = (
                            (
                                ts_base
                                + datetime.timedelta(minutes=random.randint(0, 540))
                            )
                            .isoformat()
                            .replace("+00:00", "Z")
                        )
                        row = synth_row(
                            backend,
                            test,
                            base_ns,
                            mode,
                            parallel,
                            n,
                            commit,
                            ts_iso,
                            args.os,
                            args.cpu,
                        )
                        rows.append(row)

        # Write daily NDJSON
        with ndjson_path.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r) + "\n")
        all_rows.extend(rows)

    # Write the dashboard array
    out_path = pathlib.Path(args.out)
    out_path.write_text(json.dumps(all_rows), encoding="utf-8")
    print(f"Wrote {out_path} with {len(all_rows)} rows")
    print(f"Sample day file: {ndjson_path}")


if __name__ == "__main__":
    main()
