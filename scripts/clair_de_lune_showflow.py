#!/usr/bin/env python3
"""
Clair de Lune — 90s text-FX recital for the touring rig.
Mirrors Moonlight Sonata structure: 3 movements + jam mode + seeded runs.
Assumes the Touring Rig API is running (make touring-rig-server, default :8787).
"""
import time, json, argparse, requests, math
API = "http://127.0.0.1:8787"

def post(path, payload): return requests.post(f"{API}{path}", json=payload, timeout=5).json()

def set_scene(name, seconds=0.0, curve="EaseInOut"): 
    return post("/rig/morph", {"scene": name, "seconds": float(seconds), "curve": curve})

def set_intensity(v): return post("/rig/intensity", {"value": max(0.0, min(1.2, float(v)))})

def set_metrics_link(strength): return post("/rig/metrics-link", {"strength": max(0.0, min(1.0, float(strength)))})

def macro(color=None, space=None, motion=None, crunch=None):
    m = {}
    if color  is not None:  m["macro.color"]  = float(color)
    if space  is not None:  m["macro.space"]  = float(space)
    if motion is not None:  m["macro.motion"] = float(motion)
    if crunch is not None:  m["macro.crunch"] = float(crunch)
    return post("/rig/param", {"batch": m})

def white_bloom(ms=800): return post("/rig/bloom", {"latch_ms": int(ms)})
def blackout(state=True): return post("/rig/blackout", {"state": bool(state)})

def movement_i_adagio(duration=30.0):
    # Hologram + Trails + Dust  (silver moonlight on water)
    set_scene("clair:M1_whisper")  # defined in JSON below
    set_metrics_link(0.35)
    set_intensity(0.20); macro(color=0.06, space=0.35, motion=0.15, crunch=0.0)
    t0 = time.time()
    while time.time() - t0 < duration:
        # subtle breathing (ripples)
        phase = (time.time() - t0)
        motion = 0.12 + 0.06 * math.sin(phase * 0.9)
        color  = 0.05 + 0.02 * math.sin(phase * 0.4)
        macro(motion=motion, color=color)
        time.sleep(0.08)

def movement_ii_allegretto(duration=30.0):
    # Neon Bloom + Reverb + Prism Fringe (warm ripples)
    set_scene("clair:M2_ripples")
    set_intensity(0.45); set_metrics_link(0.45)
    macro(color=0.10, space=0.55, motion=0.28, crunch=0.0)
    t0 = time.time()
    while time.time() - t0 < duration:
        # arpeggio swell — light triplets feeling
        phase = (time.time() - t0)
        space  = 0.5 + 0.15 * max(0.0, math.sin(phase * 3.0))
        color  = 0.10 + 0.06 * math.sin(phase * 0.6)
        macro(space=space, color=color)
        time.sleep(0.07)

def movement_iii_dawn(duration=30.0):
    # Glass Cathedral + Chromatic Shift + Bloom trails (dawn)
    set_scene("clair:M3_dawn")
    set_metrics_link(0.35)
    # slow rise & fall into reflection
    set_intensity(0.60); macro(color=0.14, space=0.75, motion=0.22, crunch=0.05)
    time.sleep(6.0)
    # resolution arc
    set_scene("clair:M3_resolve", seconds=6.0, curve="EaseOut")
    t0 = time.time()
    while time.time() - t0 < (duration - 8.0):
        phase = (time.time() - t0)
        space  = 0.7 + 0.1 * math.sin(phase * 0.35)
        color  = 0.12 + 0.05 * math.sin(phase * 0.25)
        macro(space=space, color=color)
        time.sleep(0.09)
    # final soft bloom ≤1s
    white_bloom(900)
    set_intensity(0.30)
    time.sleep(1.0)
    blackout(True)

def run_show(total=90, seed=None):
    # Optional deterministic seed if your rig supports it (no-op if not)
    try: post("/rig/param", {"key":"seed.value","value": int(seed) if seed else 0})
    except: pass
    # compliance: reduced motion respected by rig; we just run the movements
    movement_i_adagio(30)
    movement_ii_allegretto(30)
    movement_iii_dawn(30)

def jam_mode(minutes=3):
    # Bring up a gentle loop ready for live macros (use operator hotkeys)
    set_scene("clair:M2_ripples"); set_intensity(0.5); set_metrics_link(0.4)
    macro(color=0.12, space=0.6, motion=0.25, crunch=0.0)
    t0 = time.time()
    while time.time() - t0 < minutes * 60:
        time.sleep(0.25)  # operator rides macros/hotkeys

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["show","jam"], default="show")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--duration", type=int, default=90)
    args = ap.parse_args()
    if args.mode == "jam": jam_mode()
    else: run_show(total=args.duration, seed=args.seed)
