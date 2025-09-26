# Differential test: IR → Julia vs hand-written reference
using Test

# Include generated code (will be created by test harness)
include("generated_map_filter_reduce.jl")

# Hand-written reference implementation
function ref_sum_even_squares(xs)
    s = 0
    @inbounds for x in xs
        if x & 1 == 0  # x % 2 == 0
            s += x * x
        end
    end
    return s
end

# Test cases for different sizes
@testset "generated equals reference" begin
    test_sizes = [0, 1, 17, 100, 1003, 10000]
    
    for n in test_sizes
        xs = collect(1:n)
        expected = ref_sum_even_squares(xs)
        actual = PCS_Generated.main()
        
        @test expected == actual "Failed for n=$n: expected $expected, got $actual"
    end
    
    # Edge cases
    @test ref_sum_even_squares([]) == PCS_Generated.main()
    @test ref_sum_even_squares([1]) == PCS_Generated.main()
    @test ref_sum_even_squares([2]) == PCS_Generated.main()
end

println("✅ All differential tests passed!")
