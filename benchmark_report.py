#!/usr/bin/env python3
"""
Generate performance benchmark reports and visualizations

This script creates markdown reports from benchmark results,
including performance comparisons and trend analysis.
"""

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def format_time_ms(time_ms: float) -> str:
    """Format time in milliseconds with appropriate units"""
    if time_ms < 1:
        return f"{time_ms:.3f} ms"
    elif time_ms < 1000:
        return f"{time_ms:.2f} ms"
    else:
        return f"{time_ms/1000:.2f} s"


def format_memory_mb(memory_mb: float) -> str:
    """Format memory usage in MB"""
    if memory_mb < 1:
        return f"{memory_mb*1024:.1f} KB"
    else:
        return f"{memory_mb:.2f} MB"


def generate_performance_table(data: List[Dict[str, Any]], title: str) -> str:
    """Generate a markdown table for performance data"""
    if not data:
        return f"### {title}\n\nNo data available.\n\n"
    
    # Get all possible keys
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())
    
    # Filter out non-displayable keys
    display_keys = [k for k in all_keys if k not in ['success', 'error', 'output']]
    
    if not display_keys:
        return f"### {title}\n\nNo displayable data.\n\n"
    
    # Create table header
    header = "| " + " | ".join(display_keys) + " |"
    separator = "| " + " | ".join(["---"] * len(display_keys)) + " |"
    
    # Create table rows
    rows = []
    for item in data:
        row = []
        for key in display_keys:
            value = item.get(key, "N/A")
            if isinstance(value, float):
                if "time" in key.lower():
                    row.append(format_time_ms(value))
                elif "memory" in key.lower():
                    row.append(format_memory_mb(value))
                else:
                    row.append(f"{value:.2f}")
            else:
                row.append(str(value))
        rows.append("| " + " | ".join(row) + " |")
    
    return f"""### {title}

{header}
{separator}
{chr(10).join(rows)}

"""


def generate_benchmark_report(results_file: str, output_file: str = None) -> str:
    """Generate a comprehensive benchmark report"""
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    report = f"""# 🚀 Polyglot Code Sampler Performance Report

**Generated:** {results.get('timestamp', 'Unknown')}  
**Mode:** {results.get('mode', 'full')}  
**Python Version:** {results.get('python_version', 'Unknown')}

## 🖥️ System Information

"""
    
    if 'system_info' in results:
        sys_info = results['system_info']
        report += f"""- **CPU Cores:** {sys_info.get('cpu_count', 'Unknown')}
- **Memory:** {sys_info.get('memory_gb', 0):.1f} GB
- **Platform:** {sys_info.get('platform', 'Unknown')}

"""
    
    # Parsing Performance
    if 'parsing' in results:
        parsing = results['parsing']
        report += f"""## 🔍 Python Parsing & IR Generation

**Average Performance:**
- Parse time: {format_time_ms(parsing.get('avg_parse_time_ms', 0))}
- Type inference: {format_time_ms(parsing.get('avg_infer_time_ms', 0))}
- Total cases: {parsing.get('total_cases', 0)}

"""
        
        if 'parse_times' in parsing:
            report += generate_performance_table(
                parsing['parse_times'], 
                "Parse Times by Case"
            )
    
    # Code Generation Performance
    if 'rust_generation' in results:
        rust_gen = results['rust_generation']
        report += f"""## ⚡ Rust Code Generation

**Average Performance:**
- Sequential: {format_time_ms(rust_gen.get('avg_generation_time_ms', 0))}
- Parallel: {format_time_ms(rust_gen.get('avg_parallel_generation_time_ms', 0))}

"""
        
        if 'generation_times' in rust_gen:
            report += generate_performance_table(
                rust_gen['generation_times'], 
                "Rust Generation Times"
            )
    
    if 'typescript_generation' in results:
        ts_gen = results['typescript_generation']
        report += f"""## 📘 TypeScript Code Generation

**Average Performance:**
- Generation time: {format_time_ms(ts_gen.get('avg_generation_time_ms', 0))}

"""
        
        if 'generation_times' in ts_gen:
            report += generate_performance_table(
                ts_gen['generation_times'], 
                "TypeScript Generation Times"
            )
    
    # Execution Performance
    if 'rust_execution' in results:
        rust_exec = results['rust_execution']
        if 'avg_compilation_time_ms' in rust_exec:
            report += f"""## 🦀 Rust Execution Performance

**Average Performance:**
- Compilation: {format_time_ms(rust_exec['avg_compilation_time_ms'])}
- Execution: {format_time_ms(rust_exec['avg_execution_time_ms'])}

"""
            
            if 'compilation_times' in rust_exec:
                report += generate_performance_table(
                    rust_exec['compilation_times'], 
                    "Rust Compilation Times"
                )
    
    if 'typescript_execution' in results:
        ts_exec = results['typescript_execution']
        if 'avg_execution_time_ms' in ts_exec:
            report += f"""## 🚀 TypeScript Execution Performance

**Average Performance:**
- Execution: {format_time_ms(ts_exec['avg_execution_time_ms'])}
- Node.js time: {format_time_ms(ts_exec.get('avg_node_time_ns', 0) / 1_000_000)}

"""
            
            if 'execution_times' in ts_exec:
                report += generate_performance_table(
                    ts_exec['execution_times'], 
                    "TypeScript Execution Times"
                )
    
    # Scalability Analysis
    if 'scalability' in results:
        scalability = results['scalability']
        report += f"""## 📈 Scalability Analysis

Performance across different data sizes:

"""
        
        if 'cases' in scalability:
            report += generate_performance_table(
                scalability['cases'], 
                "Scalability by Range Size"
            )
    
    # Performance Insights
    report += """## 💡 Performance Insights

### Key Findings

"""
    
    # Add insights based on the data
    insights = []
    
    if 'rust_generation' in results and 'typescript_generation' in results:
        rust_avg = results['rust_generation'].get('avg_generation_time_ms', 0)
        ts_avg = results['typescript_generation'].get('avg_generation_time_ms', 0)
        if rust_avg > 0 and ts_avg > 0:
            ratio = rust_avg / ts_avg
            if ratio > 1.1:
                insights.append(f"TypeScript generation is {ratio:.1f}x faster than Rust generation")
            elif ratio < 0.9:
                insights.append(f"Rust generation is {1/ratio:.1f}x faster than TypeScript generation")
            else:
                insights.append("Rust and TypeScript generation have similar performance")
    
    if 'parsing' in results:
        parse_avg = results['parsing'].get('avg_parse_time_ms', 0)
        infer_avg = results['parsing'].get('avg_infer_time_ms', 0)
        if parse_avg > 0 and infer_avg > 0:
            if infer_avg > parse_avg * 0.5:
                insights.append("Type inference takes significant time - consider caching for repeated operations")
            else:
                insights.append("Type inference is fast and efficient")
    
    if 'scalability' in results and 'cases' in results['scalability']:
        cases = results['scalability']['cases']
        if len(cases) >= 2:
            small_parse = cases[0].get('parse_time_ms', 0)
            large_parse = cases[-1].get('parse_time_ms', 0)
            if small_parse > 0 and large_parse > 0:
                scale_factor = large_parse / small_parse
                data_scale = int(cases[-1].get('range_size', '0').split(',')[1]) / int(cases[0].get('range_size', '0').split(',')[1])
                if scale_factor < data_scale * 0.5:
                    insights.append("Parsing scales sub-linearly - excellent performance characteristics")
                elif scale_factor > data_scale * 2:
                    insights.append("Parsing scales super-linearly - consider optimization for large inputs")
                else:
                    insights.append("Parsing scales linearly with input size")
    
    if not insights:
        insights.append("Run more comprehensive benchmarks to generate insights")
    
    for insight in insights:
        report += f"- {insight}\n"
    
    report += """
### Recommendations

1. **For Production Use**: Consider caching parsed IR for repeated transformations
2. **For Large Datasets**: Use parallel Rust generation for better performance
3. **For Development**: TypeScript generation provides fast iteration cycles
4. **For Performance Critical**: Rust compilation overhead is offset by execution speed

---
*Report generated by Polyglot Code Sampler Benchmark Suite*
"""
    
    return report


def main():
    """Main report generator"""
    parser = argparse.ArgumentParser(description="Generate benchmark performance reports")
    parser.add_argument("--input", "-i", default="benchmark_results.json", help="Input benchmark results file")
    parser.add_argument("--output", "-o", help="Output markdown file (default: benchmark_report.md)")
    parser.add_argument("--print", action="store_true", help="Print report to stdout")
    
    args = parser.parse_args()
    
    if not Path(args.input).exists():
        print(f"Error: Benchmark results file '{args.input}' not found")
        print("Run 'make benchmark' or 'python benchmark.py' first")
        return 1
    
    report = generate_benchmark_report(args.input)
    
    if args.print:
        print(report)
    else:
        output_file = args.output or "benchmark_report.md"
        Path(output_file).write_text(report)
        print(f"📊 Performance report generated: {output_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())
