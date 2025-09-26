"""
Command-line interface for Polyglot Code Sampler
"""

import argparse
import sys
from .core import PyToIR
from .renderers.rust import render_rust
from .renderers.ts import render_ts
from .renderers.csharp import render_csharp
from .renderers.sql import render_sql

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Polyglot Code Sampler - Transform Python comprehensions across 5 ecosystems",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pcs --code "sum(i*i for i in range(10) if i%2==0)" --target rust
  pcs --code "[x*x for x in range(5)]" --target ts --parallel
  pcs --code "{x: x*x for x in range(3)}" --target csharp
  pcs --code "sum(i for i in range(100))" --target sql --execute-sql
        """
    )
    
    parser.add_argument(
        "--code", 
        required=True,
        help="Python comprehension to transform"
    )
    
    parser.add_argument(
        "--target",
        choices=["rust", "ts", "go", "csharp", "sql"],
        default="rust",
        help="Target language (default: rust)"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Enable parallel processing (Rayon/Rust, Web Workers/TS, Goroutines/Go, PLINQ/C#)"
    )
    
    parser.add_argument(
        "--sql-dialect",
        choices=["sqlite", "postgresql"],
        default="sqlite",
        help="SQL dialect (default: sqlite)"
    )
    
    parser.add_argument(
        "--execute-sql",
        action="store_true",
        help="Execute generated SQL and display results"
    )
    
    parser.add_argument(
        "--int-type",
        default="i32",
        help="Integer type for Rust (default: i32)"
    )
    
    parser.add_argument(
        "--strict-types",
        action="store_true",
        help="Enable strict type checking"
    )
    
    args = parser.parse_args()
    
    try:
        # Parse Python code to IR
        parser_obj = PyToIR()
        ir = parser_obj.parse(args.code)
        
        # Generate target code
        if args.target == "rust":
            output = render_rust(ir, parallel=args.parallel, int_type=args.int_type)
        elif args.target == "ts":
            output = render_ts(ir, parallel=args.parallel)
        elif args.target == "csharp":
            output = render_csharp(ir, parallel=args.parallel)
        elif args.target == "sql":
            output = render_sql(ir, dialect=args.sql_dialect)
            if args.execute_sql:
                execute_sql_and_display(output)
                return
        else:
            print(f"Target '{args.target}' not yet implemented", file=sys.stderr)
            sys.exit(1)
        
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
            timeout=10
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
