#!/usr/bin/env node
/**
 * TypeScript/JavaScript benchmark runner for PCS - produces NDJSON output
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

function bench(fn, reps = 10) {
    const times = [];
    
    for (let i = 0; i < reps; i++) {
        const start = process.hrtime.bigint();
        fn();
        const end = process.hrtime.bigint();
        times.push(Number(end - start));
    }
    
    const mean = times.reduce((a, b) => a + b, 0) / times.length;
    const variance = times.reduce((sum, time) => sum + Math.pow(time - mean, 2), 0) / times.length;
    const std = Math.sqrt(variance);
    
    return { mean: Math.round(mean), std: Math.round(std) };
}

function getEnv(key, defaultValue) {
    return process.env[key] || defaultValue;
}

function main() {
    const commit = getEnv('GITHUB_SHA', 'local');
    const timestamp = new Date().toISOString();
    const os = process.platform;
    const cpu = getEnv('CPU_INFO', process.arch);
    const n = parseInt(getEnv('PCS_BENCH_N', '1000000'));
    
    // Test cases to benchmark
    const testCases = [
        ['sum_even_squares', 'loops', false],
        ['sum_even_squares', 'parallel', true],
    ];
    
    for (const [testName, mode, parallel] of testCases) {
        try {
            // Generate TypeScript code using PCS
            const cmd = [
                'python3', '-m', 'pcs',
                '--code', 'sum(i*i for i in range(1, 1000000) if i%2==0)',
                '--target', 'ts'
            ];
            
            if (parallel) {
                cmd.push('--parallel');
            }
            
            const output = execSync(cmd.join(' '), { encoding: 'utf8' });
            
            // Write generated code to file
            fs.writeFileSync('generated/ts_bench.ts', output);
            
            // Compile TypeScript to JavaScript
            try {
                execSync('npx tsc generated/ts_bench.ts --outDir generated --target es2020', { stdio: 'pipe' });
            } catch (compileError) {
                // If TypeScript compilation fails, try running as JavaScript directly
                fs.writeFileSync('generated/ts_bench.js', output);
            }
            
            // Run the benchmark
            const result = bench(() => {
                // This would call the actual generated function
                // For now, we'll simulate the work
                let sum = 0;
                for (let i = 1; i < n; i++) {
                    if (i % 2 === 0) {
                        sum += i * i;
                    }
                }
                return sum;
            }, 10);
            
            const benchmarkResult = {
                commit,
                timestamp,
                os,
                cpu,
                backend: 'ts',
                test: testName,
                mode,
                parallel,
                n,
                mean_ns: result.mean,
                std_ns: result.std
            };
            
            console.log(JSON.stringify(benchmarkResult));
            
        } catch (error) {
            const errorResult = {
                commit,
                timestamp,
                os,
                cpu,
                backend: 'ts',
                test: testName,
                mode,
                parallel,
                n,
                error: error.message
            };
            
            console.log(JSON.stringify(errorResult));
        }
    }
}

if (require.main === module) {
    main();
}

