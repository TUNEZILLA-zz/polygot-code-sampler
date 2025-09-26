#!/usr/bin/env julia
"""
Julia benchmark runner for PCS - produces NDJSON output
"""

using JSON3, Statistics, Dates

# Simple micro-bench without external deps
function bench(f, reps=10)
    ts = Vector{Float64}(undef, reps)
    for i in 1:reps
        t1 = time_ns()
        f()
        t2 = time_ns()
        ts[i] = (t2 - t1)
    end
    (; mean=mean(ts), std=std(ts))
end

# Get environment variables
commit = get(ENV, "GITHUB_SHA", "local")
timestamp = Dates.format(now(UTC), dateformat"yyyy-mm-ddTHH:MM:SSZ")
os = Sys.KERNEL
cpu = get(ENV, "CPU_INFO", Sys.CPU_NAME)
N = parse(Int, get(ENV, "PCS_BENCH_N", "1000000"))

# Test cases to benchmark
test_cases = [
    ("sum_even_squares", "loops", false),
    ("sum_even_squares", "broadcast", false),
    ("sum_even_squares", "loops", true),
    ("dict_comp_sharded", "loops", true),
]

for (test_name, mode, parallel) in test_cases
    try
        # Generate Julia code using PCS
        cmd = `julia -e "
            using Pkg
            Pkg.activate(\".\")
            include(\"pcs/__init__.py\")
            import PCS
            import subprocess
            import sys
            
            # Generate Julia code
            result = subprocess.run([
                sys.executable, \"-m\", \"pcs\", 
                \"--code\", \"sum(i*i for i in range(1, $N) if i%2==0)\",
                \"--target\", \"julia\",
                \"--mode\", \"$mode\"
                $(parallel ? ", \"--parallel\"" : "")
            ], capture_output=true, text=true)
            
            if result.returncode == 0
                open(\"generated/$(test_name)_$(mode).jl\", \"w\") do f
                    write(f, result.stdout)
                end
            else
                println(stderr, \"Failed to generate Julia code: \", result.stderr)
                exit(1)
            end
        "`
        
        run(cmd)
        
        # Include generated code
        include("generated/$(test_name)_$(mode).jl")
        
        # Benchmark the generated function
        res = bench(() -> PCS_Generated.main(), 10)
        
        # Output NDJSON line
        result = Dict(
            "commit" => commit,
            "timestamp" => timestamp,
            "os" => os,
            "cpu" => cpu,
            "backend" => "julia",
            "test" => test_name,
            "mode" => mode,
            "parallel" => parallel,
            "n" => N,
            "mean_ns" => round(Int, res.mean),
            "std_ns" => round(Int, res.std)
        )
        
        println(JSON3.write(result))
        
    catch e
        # Output error as JSON for debugging
        error_result = Dict(
            "commit" => commit,
            "timestamp" => timestamp,
            "os" => os,
            "cpu" => cpu,
            "backend" => "julia",
            "test" => test_name,
            "mode" => mode,
            "parallel" => parallel,
            "n" => N,
            "error" => string(e)
        )
        println(JSON3.write(error_result))
    end
end
