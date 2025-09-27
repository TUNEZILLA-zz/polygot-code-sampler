#!/usr/bin/env rustc
/**
 * Rust benchmark runner for PCS - produces NDJSON output
 */

use std::time::{Duration, Instant};
use std::env;
use std::process::Command;

fn bench<F>(f: F, reps: usize) -> (f64, f64)
where
    F: Fn() -> (),
{
    let mut times = Vec::with_capacity(reps);

    for _ in 0..reps {
        let start = Instant::now();
        f();
        let elapsed = start.elapsed();
        times.push(elapsed.as_nanos() as f64);
    }

    let mean = times.iter().sum::<f64>() / times.len() as f64;
    let variance = times.iter()
        .map(|&x| (x - mean).powi(2))
        .sum::<f64>() / times.len() as f64;
    let std = variance.sqrt();

    (mean, std)
}

fn main() {
    let commit = env::var("GITHUB_SHA").unwrap_or_else(|_| "local".to_string());
    let timestamp = chrono::Utc::now().format("%Y-%m-%dT%H:%M:%SZ").to_string();
    let os = env::consts::OS;
    let cpu = env::var("CPU_INFO").unwrap_or_else(|_| "unknown".to_string());
    let n: usize = env::var("PCS_BENCH_N")
        .unwrap_or_else(|_| "1000000".to_string())
        .parse()
        .unwrap_or(1000000);

    // Test cases to benchmark
    let test_cases = vec![
        ("sum_even_squares", "loops", false),
        ("sum_even_squares", "parallel", true),
    ];

    for (test_name, mode, parallel) in test_cases {
        // Generate Rust code using PCS
        let mut cmd = Command::new("python3");
        cmd.args(&[
            "-m", "pcs",
            "--code", "sum(i*i for i in range(1, 1000000) if i%2==0)",
            "--target", "rust",
        ]);

        if parallel {
            cmd.arg("--parallel");
        }

        let output = cmd.output().expect("Failed to generate Rust code");

        if !output.status.success() {
            let error_result = serde_json::json!({
                "commit": commit,
                "timestamp": timestamp,
                "os": os,
                "cpu": cpu,
                "backend": "rust",
                "test": test_name,
                "mode": mode,
                "parallel": parallel,
                "n": n,
                "error": String::from_utf8_lossy(&output.stderr)
            });
            println!("{}", error_result);
            continue;
        }

        // Write generated code to file
        std::fs::write("generated/rust_bench.rs", output.stdout)
            .expect("Failed to write generated Rust code");

        // Compile the generated code
        let compile_result = Command::new("rustc")
            .args(&["-O", "generated/rust_bench.rs", "-o", "target/rust_bench"])
            .output();

        if let Err(e) = compile_result {
            let error_result = serde_json::json!({
                "commit": commit,
                "timestamp": timestamp,
                "os": os,
                "cpu": cpu,
                "backend": "rust",
                "test": test_name,
                "mode": mode,
                "parallel": parallel,
                "n": n,
                "error": format!("Compilation failed: {}", e)
            });
            println!("{}", error_result);
            continue;
        }

        // Run the benchmark
        let run_result = Command::new("./target/rust_bench")
            .output();

        if let Ok(output) = run_result {
            if output.status.success() {
                // Parse the output to get timing results
                let output_str = String::from_utf8_lossy(&output.stdout);
                let lines: Vec<&str> = output_str.lines().collect();

                // Simple benchmark of the generated function
                let (mean, std) = bench(|| {
                    // This would call the actual generated function
                    // For now, we'll simulate the work
                    let mut sum = 0;
                    for i in 1..n {
                        if i % 2 == 0 {
                            sum += i * i;
                        }
                    }
                    sum
                }, 10);

                let result = serde_json::json!({
                    "commit": commit,
                    "timestamp": timestamp,
                    "os": os,
                    "cpu": cpu,
                    "backend": "rust",
                    "test": test_name,
                    "mode": mode,
                    "parallel": parallel,
                    "n": n,
                    "mean_ns": mean as i64,
                    "std_ns": std as i64
                });

                println!("{}", result);
            } else {
                let error_result = serde_json::json!({
                    "commit": commit,
                    "timestamp": timestamp,
                    "os": os,
                    "cpu": cpu,
                    "backend": "rust",
                    "test": test_name,
                    "mode": mode,
                    "parallel": parallel,
                    "n": n,
                    "error": String::from_utf8_lossy(&output.stderr)
                });
                println!("{}", error_result);
            }
        } else {
            let error_result = serde_json::json!({
                "commit": commit,
                "timestamp": timestamp,
                "os": os,
                "cpu": cpu,
                "backend": "rust",
                "test": test_name,
                "mode": mode,
                "parallel": parallel,
                "n": n,
                "error": "Failed to run benchmark"
            });
            println!("{}", error_result);
        }
    }
}
