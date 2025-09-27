#!/usr/bin/env python3
"""
Performance benchmarks for Polyglot Code Sampler

This module provides comprehensive benchmarking of:
1. Python AST parsing and IR generation
2. Rust code generation and compilation
3. TypeScript code generation and execution
4. Parallel vs sequential performance
5. Memory usage and scalability
"""

import argparse
import json
import platform
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

import psutil

from pcs_step3_ts import (
    PyToIR,
    infer_types,
    render_go,
    render_rust,
    render_sql,
    render_ts,
)


class BenchmarkSuite:
    """Comprehensive benchmark suite for Polyglot Code Sampler"""

    def __init__(self):
        self.results: Dict[str, Any] = {}
        self.temp_dir = Path(tempfile.mkdtemp(prefix="pcs_benchmark_"))

    def cleanup(self):
        """Clean up temporary files"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def measure_memory(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """Measure memory usage during function execution"""
        process = psutil.Process()
        mem_before = process.memory_info().rss / 1024 / 1024  # MB

        result = func(*args, **kwargs)

        mem_after = process.memory_info().rss / 1024 / 1024  # MB
        mem_used = mem_after - mem_before

        return result, mem_used

    def benchmark_parsing(self, test_cases: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Benchmark Python AST parsing and IR generation"""
        print("🔍 Benchmarking Python parsing and IR generation...")

        parser = PyToIR()
        results = {
            "total_cases": len(test_cases),
            "parse_times": [],
            "ir_generation_times": [],
            "type_inference_times": [],
            "memory_usage": [],
        }

        for code, name in test_cases:
            # Benchmark parsing
            start_time = time.perf_counter()
            ir, mem_parse = self.measure_memory(parser.parse, code)
            parse_time = time.perf_counter() - start_time

            # Benchmark type inference
            start_time = time.perf_counter()
            type_info, mem_infer = self.measure_memory(infer_types, ir)
            infer_time = time.perf_counter() - start_time

            results["parse_times"].append(
                {"case": name, "time_ms": parse_time * 1000, "memory_mb": mem_parse}
            )

            results["ir_generation_times"].append(
                {"case": name, "time_ms": parse_time * 1000}  # Same as parsing for now
            )

            results["type_inference_times"].append(
                {"case": name, "time_ms": infer_time * 1000, "memory_mb": mem_infer}
            )

        # Calculate averages
        results["avg_parse_time_ms"] = sum(
            r["time_ms"] for r in results["parse_times"]
        ) / len(results["parse_times"])
        results["avg_infer_time_ms"] = sum(
            r["time_ms"] for r in results["type_inference_times"]
        ) / len(results["type_inference_times"])

        return results

    def benchmark_rust_generation(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark Rust code generation"""
        print("🦀 Benchmarking Rust code generation...")

        parser = PyToIR()
        results = {
            "total_cases": len(test_cases),
            "generation_times": [],
            "parallel_generation_times": [],
        }

        for code, name in test_cases:
            ir = parser.parse(code)
            type_info = infer_types(ir)

            # Sequential generation
            start_time = time.perf_counter()
            rust_code = render_rust(ir, func_name=name, type_info=type_info)
            seq_time = time.perf_counter() - start_time

            # Parallel generation
            start_time = time.perf_counter()
            rust_parallel = render_rust(
                ir, func_name=name, parallel=True, type_info=type_info
            )
            par_time = time.perf_counter() - start_time

            results["generation_times"].append(
                {
                    "case": name,
                    "time_ms": seq_time * 1000,
                    "code_size_chars": len(rust_code),
                }
            )

            results["parallel_generation_times"].append(
                {
                    "case": name,
                    "time_ms": par_time * 1000,
                    "code_size_chars": len(rust_parallel),
                }
            )

        results["avg_generation_time_ms"] = sum(
            r["time_ms"] for r in results["generation_times"]
        ) / len(results["generation_times"])
        results["avg_parallel_generation_time_ms"] = sum(
            r["time_ms"] for r in results["parallel_generation_times"]
        ) / len(results["parallel_generation_times"])

        return results

    def benchmark_typescript_generation(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark TypeScript code generation"""
        print("📘 Benchmarking TypeScript code generation...")

        parser = PyToIR()
        results = {"total_cases": len(test_cases), "generation_times": []}

        for code, name in test_cases:
            ir = parser.parse(code)
            type_info = infer_types(ir)

            start_time = time.perf_counter()
            ts_code = render_ts(ir, func_name=name, type_info=type_info)
            gen_time = time.perf_counter() - start_time

            results["generation_times"].append(
                {
                    "case": name,
                    "time_ms": gen_time * 1000,
                    "code_size_chars": len(ts_code),
                }
            )

        results["avg_generation_time_ms"] = sum(
            r["time_ms"] for r in results["generation_times"]
        ) / len(results["generation_times"])

        return results

    def benchmark_sql_generation(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark SQL code generation"""
        print("🗄️ Benchmarking SQL code generation...")

        parser = PyToIR()
        results = {"total_cases": len(test_cases), "generation_times": []}

        for code, name in test_cases:
            ir = parser.parse(code)

            start_time = time.perf_counter()
            sql_code = render_sql(ir, func_name=name)
            gen_time = time.perf_counter() - start_time

            results["generation_times"].append(
                {
                    "case": name,
                    "time_ms": gen_time * 1000,
                    "code_size_chars": len(sql_code),
                }
            )

        results["avg_generation_time_ms"] = sum(
            r["time_ms"] for r in results["generation_times"]
        ) / len(results["generation_times"])

        return results

    def benchmark_go_generation(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark Go code generation"""
        print("🐹 Benchmarking Go code generation...")

        parser = PyToIR()
        results = {"total_cases": len(test_cases), "generation_times": []}

        for code, name in test_cases:
            ir = parser.parse(code)

            start_time = time.perf_counter()
            go_code = render_go(ir, func_name=name)
            gen_time = time.perf_counter() - start_time

            results["generation_times"].append(
                {
                    "case": name,
                    "time_ms": gen_time * 1000,
                    "code_size_chars": len(go_code),
                }
            )

        results["avg_generation_time_ms"] = sum(
            r["time_ms"] for r in results["generation_times"]
        ) / len(results["generation_times"])

        return results

    def benchmark_go_parallel_generation(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark Go parallel code generation"""
        print("🚀 Benchmarking Go parallel code generation...")

        parser = PyToIR()
        results = {"total_cases": len(test_cases), "generation_times": []}

        for code, name in test_cases:
            ir = parser.parse(code)

            start_time = time.perf_counter()
            go_code = render_go(ir, func_name=name, parallel=True)
            gen_time = time.perf_counter() - start_time

            results["generation_times"].append(
                {
                    "case": name,
                    "time_ms": gen_time * 1000,
                    "code_size_chars": len(go_code),
                }
            )

        results["avg_generation_time_ms"] = sum(
            r["time_ms"] for r in results["generation_times"]
        ) / len(results["generation_times"])

        return results

    def benchmark_rust_execution(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark Rust compilation and execution"""
        print("⚡ Benchmarking Rust compilation and execution...")

        parser = PyToIR()
        results = {
            "total_cases": len(test_cases),
            "compilation_times": [],
            "execution_times": [],
            "parallel_execution_times": [],
        }

        for code, name in test_cases:
            ir = parser.parse(code)
            type_info = infer_types(ir)

            # Generate Rust code
            rust_code = render_rust(ir, func_name=name, type_info=type_info)
            render_rust(ir, func_name=name, parallel=True, type_info=type_info)

            # Create Rust project
            rust_dir = self.temp_dir / f"rust_{name}"
            rust_dir.mkdir(exist_ok=True)

            # Write Cargo.toml
            cargo_toml = f"""[package]
name = "{name}"
version = "0.1.0"
edition = "2021"

[dependencies]
rayon = "1.8"
"""
            (rust_dir / "Cargo.toml").write_text(cargo_toml)

            # Write main.rs
            main_rs = f"""fn main() {{
    let result = {name}();
    println!("{{}}", result);
}}

{rust_code}
"""
            (rust_dir / "src").mkdir(exist_ok=True)
            (rust_dir / "src" / "main.rs").write_text(main_rs)

            # Benchmark compilation
            start_time = time.perf_counter()
            try:
                subprocess.run(
                    ["cargo", "build", "--release"],
                    cwd=rust_dir,
                    capture_output=True,
                    check=True,
                    timeout=30,
                )
                compile_time = time.perf_counter() - start_time

                # Benchmark execution
                start_time = time.perf_counter()
                result = subprocess.run(
                    ["cargo", "run", "--release"],
                    cwd=rust_dir,
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                exec_time = time.perf_counter() - start_time

                results["compilation_times"].append(
                    {"case": name, "time_ms": compile_time * 1000, "success": True}
                )

                results["execution_times"].append(
                    {
                        "case": name,
                        "time_ms": exec_time * 1000,
                        "output": result.stdout.strip(),
                        "success": result.returncode == 0,
                    }
                )

            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
                results["compilation_times"].append(
                    {"case": name, "time_ms": 0, "success": False, "error": str(e)}
                )

                results["execution_times"].append(
                    {"case": name, "time_ms": 0, "success": False, "error": str(e)}
                )

        # Calculate averages for successful cases
        successful_compiles = [r for r in results["compilation_times"] if r["success"]]
        successful_execs = [r for r in results["execution_times"] if r["success"]]

        if successful_compiles:
            results["avg_compilation_time_ms"] = sum(
                r["time_ms"] for r in successful_compiles
            ) / len(successful_compiles)
        if successful_execs:
            results["avg_execution_time_ms"] = sum(
                r["time_ms"] for r in successful_execs
            ) / len(successful_execs)

        return results

    def benchmark_typescript_execution(
        self, test_cases: List[Tuple[str, str]]
    ) -> Dict[str, Any]:
        """Benchmark TypeScript execution with Node.js"""
        print("🚀 Benchmarking TypeScript execution...")

        parser = PyToIR()
        results = {"total_cases": len(test_cases), "execution_times": []}

        for code, name in test_cases:
            ir = parser.parse(code)
            type_info = infer_types(ir)

            # Generate TypeScript code
            ts_code = render_ts(ir, func_name=name, type_info=type_info)

            # Create Node.js script
            node_script = f"""
{ts_code}

// Benchmark execution
const start = process.hrtime.bigint();
const result = {name}();
const end = process.hrtime.bigint();

console.log(JSON.stringify({{
    result: result,
    execution_time_ns: Number(end - start)
}}));
"""

            ts_file = self.temp_dir / f"{name}.js"
            ts_file.write_text(node_script)

            # Benchmark execution
            start_time = time.perf_counter()
            try:
                result = subprocess.run(
                    ["node", str(ts_file)], capture_output=True, text=True, timeout=10
                )
                exec_time = time.perf_counter() - start_time

                if result.returncode == 0:
                    output_data = json.loads(result.stdout.strip())
                    results["execution_times"].append(
                        {
                            "case": name,
                            "time_ms": exec_time * 1000,
                            "node_time_ns": output_data["execution_time_ns"],
                            "output": output_data["result"],
                            "success": True,
                        }
                    )
                else:
                    results["execution_times"].append(
                        {
                            "case": name,
                            "time_ms": exec_time * 1000,
                            "success": False,
                            "error": result.stderr,
                        }
                    )

            except (
                subprocess.TimeoutExpired,
                subprocess.CalledProcessError,
                json.JSONDecodeError,
            ) as e:
                results["execution_times"].append(
                    {"case": name, "time_ms": 0, "success": False, "error": str(e)}
                )

        # Calculate averages for successful cases
        successful_execs = [r for r in results["execution_times"] if r["success"]]
        if successful_execs:
            results["avg_execution_time_ms"] = sum(
                r["time_ms"] for r in successful_execs
            ) / len(successful_execs)
            results["avg_node_time_ns"] = sum(
                r["node_time_ns"] for r in successful_execs
            ) / len(successful_execs)

        return results

    def benchmark_scalability(self) -> Dict[str, Any]:
        """Benchmark performance with increasing data sizes"""
        print("📈 Benchmarking scalability...")

        scalability_cases = [
            ("squares = [x**2 for x in range(100)]", "small"),
            ("squares = [x**2 for x in range(1000)]", "medium"),
            ("squares = [x**2 for x in range(10000)]", "large"),
            ("squares = [x**2 for x in range(100000)]", "xlarge"),
        ]

        results = {"cases": [], "parse_times": [], "generation_times": []}

        parser = PyToIR()

        for code, size in scalability_cases:
            # Benchmark parsing
            start_time = time.perf_counter()
            ir = parser.parse(code)
            parse_time = time.perf_counter() - start_time

            # Benchmark generation
            start_time = time.perf_counter()
            type_info = infer_types(ir)
            rust_code = render_rust(ir, func_name=f"test_{size}", type_info=type_info)
            gen_time = time.perf_counter() - start_time

            results["cases"].append(
                {
                    "size": size,
                    "range_size": code.split("range(")[1].split(")")[0],
                    "parse_time_ms": parse_time * 1000,
                    "generation_time_ms": gen_time * 1000,
                    "code_size_chars": len(rust_code),
                }
            )

        return results

    def run_full_benchmark(self) -> Dict[str, Any]:
        """Run complete benchmark suite"""
        print("🚀 Starting comprehensive benchmark suite...")

        # Define test cases
        test_cases = [
            ("squares = [x**2 for x in range(10)]", "simple_squares"),
            ("odds = {i: i*i for i in range(1,6) if i % 2 == 1}", "dict_odds"),
            (
                "pairs = {(i, j) for i in range(3) for j in range(3) if i != j}",
                "nested_pairs",
            ),
            ("total = sum(x for x in range(100) if x % 2 == 0)", "sum_reduction"),
            ("best = max(i*j for i in range(10) for j in range(10))", "max_reduction"),
            ("has_odd = any(x % 2 == 1 for x in range(1,100))", "any_reduction"),
        ]

        # Run all benchmarks
        self.results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "python_version": f"{psutil.Process().cmdline()[0]}",
            "system_info": {
                "cpu_count": psutil.cpu_count(),
                "memory_gb": psutil.virtual_memory().total / (1024**3),
                "platform": platform.platform(),
            },
            "parsing": self.benchmark_parsing(test_cases),
            "rust_generation": self.benchmark_rust_generation(test_cases),
            "typescript_generation": self.benchmark_typescript_generation(test_cases),
            "sql_generation": self.benchmark_sql_generation(test_cases),
            "go_generation": self.benchmark_go_generation(test_cases),
            "go_parallel_generation": self.benchmark_go_parallel_generation(test_cases),
            "rust_execution": self.benchmark_rust_execution(test_cases),
            "typescript_execution": self.benchmark_typescript_execution(test_cases),
            "scalability": self.benchmark_scalability(),
        }

        return self.results

    def save_results(self, filename: str = "benchmark_results.json"):
        """Save benchmark results to file"""
        output_file = Path(filename)
        output_file.write_text(json.dumps(self.results, indent=2))
        print(f"📊 Results saved to {output_file}")

    def print_summary(self):
        """Print benchmark summary"""
        if not self.results:
            print("No benchmark results available")
            return

        print("\n" + "=" * 80)
        print("🏆 BENCHMARK SUMMARY")
        print("=" * 80)

        # Parsing performance
        parsing = self.results["parsing"]
        print("\n🔍 Python Parsing & IR Generation:")
        print(f"   Average parse time: {parsing['avg_parse_time_ms']:.2f} ms")
        print(f"   Average type inference: {parsing['avg_infer_time_ms']:.2f} ms")

        # Code generation performance
        rust_gen = self.results["rust_generation"]
        ts_gen = self.results["typescript_generation"]
        sql_gen = self.results["sql_generation"]
        go_gen = self.results["go_generation"]
        go_par_gen = self.results.get("go_parallel_generation", {})
        print("\n⚡ Code Generation:")
        print(f"   Rust (sequential): {rust_gen['avg_generation_time_ms']:.2f} ms")
        print(
            f"   Rust (parallel): {rust_gen['avg_parallel_generation_time_ms']:.2f} ms"
        )
        print(f"   TypeScript: {ts_gen['avg_generation_time_ms']:.2f} ms")
        print(f"   SQL: {sql_gen['avg_generation_time_ms']:.2f} ms")
        print(f"   Go (sequential): {go_gen['avg_generation_time_ms']:.2f} ms")
        if go_par_gen:
            print(f"   Go (parallel): {go_par_gen['avg_generation_time_ms']:.2f} ms")

        # Execution performance
        if (
            "rust_execution" in self.results
            and "avg_compilation_time_ms" in self.results["rust_execution"]
        ):
            rust_exec = self.results["rust_execution"]
            print("\n🦀 Rust Execution:")
            print(
                f"   Average compilation: {rust_exec['avg_compilation_time_ms']:.2f} ms"
            )
            print(f"   Average execution: {rust_exec['avg_execution_time_ms']:.2f} ms")

        if (
            "typescript_execution" in self.results
            and "avg_execution_time_ms" in self.results["typescript_execution"]
        ):
            ts_exec = self.results["typescript_execution"]
            print("\n📘 TypeScript Execution:")
            print(f"   Average execution: {ts_exec['avg_execution_time_ms']:.2f} ms")
            print(
                f"   Average Node.js time: {ts_exec['avg_node_time_ns'] / 1_000_000:.2f} ms"
            )

        # Scalability
        if "scalability" in self.results:
            scalability = self.results["scalability"]
            print("\n📈 Scalability (range sizes):")
            for case in scalability["cases"]:
                print(
                    f"   {case['range_size']}: parse={case['parse_time_ms']:.2f}ms, gen={case['generation_time_ms']:.2f}ms"
                )


def main():
    """Main benchmark runner"""
    parser = argparse.ArgumentParser(
        description="Polyglot Code Sampler Performance Benchmarks"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="benchmark_results.json",
        help="Output file for results",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick benchmark (skip execution tests)",
    )
    args = parser.parse_args()

    suite = BenchmarkSuite()

    try:
        if args.quick:
            print("🏃 Running quick benchmark...")
            # Quick benchmark - just parsing and generation
            test_cases = [
                ("squares = [x**2 for x in range(10)]", "simple_squares"),
                ("odds = {i: i*i for i in range(1,6) if i % 2 == 1}", "dict_odds"),
            ]

            suite.results = {
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "mode": "quick",
                "parsing": suite.benchmark_parsing(test_cases),
                "rust_generation": suite.benchmark_rust_generation(test_cases),
                "typescript_generation": suite.benchmark_typescript_generation(
                    test_cases
                ),
                "sql_generation": suite.benchmark_sql_generation(test_cases),
                "go_generation": suite.benchmark_go_generation(test_cases),
                "go_parallel_generation": suite.benchmark_go_parallel_generation(
                    test_cases
                ),
            }
        else:
            suite.run_full_benchmark()

        suite.print_summary()
        suite.save_results(args.output)

    finally:
        suite.cleanup()


if __name__ == "__main__":
    main()
