# Property tests for PCS generated Julia code
# Run with: julia --project -e 'include("examples/julia/property_tests.jl")'

using Test, Random
Random.seed!(0)

# Sequential implementation
function seq_sum_even_sq(n)
    acc = 0
    @inbounds for i in 1:n
        if i & 1 == 0  # i % 2 == 0
            acc += i * i
        end
    end
    acc
end

# Parallel implementation (thread-safe)
function par_sum_even_sq(n)
    parts = fill(0, Threads.nthreads())
    @threads for i in 1:n
        if i & 1 == 0  # i % 2 == 0
            parts[threadid()] += i * i
        end
    end
    s = 0
    @inbounds for p in parts; s += p; end
    s
end

# Sequential dict comprehension
function seq_dict_comp(n)
    result = Dict{Int, Int}()
    for i in 1:n
        if i % 2 == 0
            result[i] = i * i
        end
    end
    result
end

# Parallel dict comprehension (shard pattern)
function par_dict_comp(n)
    shards = [Dict{Int, Int}() for _ in 1:Threads.nthreads()]
    @threads for i in 1:n
        if i % 2 == 0
            shards[threadid()][i] = i * i
        end
    end
    result = Dict{Int, Int}()
    @inbounds for s in shards
        for (k, v) in s
            result[k] = v
        end
    end
    result
end

# Sequential max reduction
function seq_max_even(n)
    acc = typemin(Int)
    for i in 1:n
        if i % 2 == 0
            acc = max(acc, i)
        end
    end
    acc
end

# Parallel max reduction
function par_max_even(n)
    parts = fill(typemin(Int), Threads.nthreads())
    @threads for i in 1:n
        if i % 2 == 0
            parts[threadid()] = max(parts[threadid()], i)
        end
    end
    acc = typemin(Int)
    @inbounds for p in parts
        acc = max(acc, p)
    end
    acc
end

@testset "PCS Julia Backend Property Tests" begin
    @testset "Parallel equals sequential - sum of even squares" begin
        for n in [100, 1000, 10000]
            @test seq_sum_even_sq(n) == par_sum_even_sq(n)
        end
    end

    @testset "Parallel equals sequential - dict comprehension" begin
        for n in [100, 1000, 10000]
            seq_result = seq_dict_comp(n)
            par_result = par_dict_comp(n)
            @test seq_result == par_result
        end
    end

    @testset "Parallel equals sequential - max reduction" begin
        for n in [100, 1000, 10000]
            @test seq_max_even(n) == par_max_even(n)
        end
    end

    @testset "Edge cases" begin
        # Empty range
        @test seq_sum_even_sq(0) == par_sum_even_sq(0)
        @test seq_dict_comp(0) == par_dict_comp(0)

        # Single element
        @test seq_sum_even_sq(1) == par_sum_even_sq(1)
        @test seq_dict_comp(1) == par_dict_comp(1)

        # All odd (no matches)
        @test seq_sum_even_sq(99) == par_sum_even_sq(99)
        @test seq_dict_comp(99) == par_dict_comp(99)
    end
end

println("✅ All property tests passed!")
println("Thread count: ", Threads.nthreads())
println("Use JULIA_NUM_THREADS to control thread count")
