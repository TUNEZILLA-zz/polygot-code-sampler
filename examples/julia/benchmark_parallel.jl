# Julia micro-benchmark harness for PCS generated code
# Run with: julia --project -e 'include("examples/julia/benchmark_parallel.jl")'

using BenchmarkTools

# Sequential version
function seq()
    acc = 0
    @inbounds for i in 1:10^7
        if i & 1 == 0  # i % 2 == 0
            acc += i
        end
    end
    acc
end

# Thread-safe parallel version
function thr()
    parts = fill(0, Threads.nthreads())
    @threads for i in 1:10^7
        if i & 1 == 0  # i % 2 == 0
            parts[threadid()] += i
        end
    end
    s = 0
    @inbounds for p in parts; s += p; end
    s
end

# Verify correctness
println("Correctness check:")
println("seq() == thr(): ", seq() == thr())
println("seq() result: ", seq())
println("thr() result: ", thr())

# Benchmark
println("\nBenchmarks:")
println("Sequential:")
@btime seq()

println("Parallel:")
@btime thr()

println("\nThread count: ", Threads.nthreads())
println("Use JULIA_NUM_THREADS to control thread count")
