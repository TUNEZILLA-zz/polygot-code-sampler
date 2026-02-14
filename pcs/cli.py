"""
Command-line interface for Polyglot Code Sampler
"""

import argparse
import sys

from .core import PyToIR
from .renderer_api import render as render_generic


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Polyglot Code Sampler - Transform Python comprehensions across 6 ecosystems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pcs --code "sum(i*i for i in range(10) if i%2==0)" --target rust
  pcs --code "[x*x for x in range(5)]" --target ts --parallel
  pcs --code "{x: x*x for x in range(3)}" --target csharp
  pcs --code "sum(i for i in range(100))" --target sql --execute-sql
        """,
    )

    parser.add_argument(
        "--code", required=True, help="Python comprehension to transform"
    )

    parser.add_argument(
        "--target",
        choices=["rust", "ts", "go", "csharp", "sql", "julia"],
        default="rust",
        help="Target language (default: rust)",
    )

    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Enable parallel processing (Rayon/Rust, Web Workers/TS, Goroutines/Go, PLINQ/C#, Threads/Julia)",
    )
    parser.add_argument(
        "--mode",
        choices=["auto", "loops", "broadcast"],
        default="auto",
        help="Julia mode: auto (heuristic), loops (explicit), or broadcast (vectorized)",
    )
    parser.add_argument(
        "--threads",
        type=int,
        help="Number of threads (pass-through to JULIA_NUM_THREADS)",
    )
    parser.add_argument(
        "--unsafe", action="store_true", help="Enable @inbounds/@simd optimizations"
    )
    parser.add_argument(
        "--no-explain",
        action="store_true",
        help="Disable explanatory comments in generated code",
    )

    parser.add_argument(
        "--sql-dialect",
        choices=["sqlite", "postgresql"],
        default="sqlite",
        help="SQL dialect (default: sqlite)",
    )

    parser.add_argument(
        "--execute-sql",
        action="store_true",
        help="Execute generated SQL and display results",
    )

    parser.add_argument(
        "--int-type", default="i32", help="Integer type for Rust (default: i32)"
    )

    parser.add_argument(
        "--strict-types", action="store_true", help="Enable strict type checking"
    )

    args = parser.parse_args()

    try:
        # Parse Python code to IR
        parser_obj = PyToIR()
        ir = parser_obj.parse(args.code)

        # Generate target code using the adapter
        output = render_generic(
            args.target,
            ir,
            parallel=args.parallel,
            mode=getattr(args, "mode", None),
            unsafe=getattr(args, "unsafe", False),
            explain=not getattr(args, "no_explain", False),
            dialect=getattr(args, "sql_dialect", None),
            int_type=getattr(args, "int_type", None),
        )

        if args.target == "sql" and args.execute_sql:
            execute_sql_and_display(output)
            return

        print(output)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def execute_sql_and_display(sql: str):
    """Execute SQL and display results"""
    import subprocess

    try:
        result = subprocess.run(
            ["sqlite3", ":memory:"],
            input=sql,
            text=True,
            capture_output=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("SQL Results:")
            print(result.stdout)
        else:
            print(f"SQL Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("SQL execution timed out")
    except FileNotFoundError:
        print("sqlite3 not found. Install SQLite to use --execute-sql")
    except Exception as e:
        print(f"Error executing SQL: {e}")


if __name__ == "__main__":
    main()
