# Sanity performance check for PCS-generated Julia code
# Run with: julia --project -e 'include("examples/julia/sanity_perf_check.jl")'

using BenchmarkTools, Base.Threads

N = 10^7
xs = collect(1:N)

function seq(xs)
    s = 0
    @inbounds for i in xs
        if i & 1 == 0; s += i*i; end
    end; s
end

function par(xs)
    parts = fill(0, nthreads())
    @threads for i in eachindex(xs)
        x = xs[i]
        if x & 1 == 0; parts[threadid()] += x*x; end
    end
    s = 0; @inbounds for p in parts; s += p; end; s
end

# Correctness check
@assert seq(xs) == par(xs)
println("✅ Correctness check passed: seq(xs) == par(xs)")

# Performance benchmarks
println("\n📊 Performance Benchmarks:")
println("Sequential:")
@btime seq($xs)

println("Parallel:")
@btime par($xs)

println("\nThread count: ", Threads.nthreads())
println("Use JULIA_NUM_THREADS to control thread count")

