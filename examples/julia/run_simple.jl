# Julia smoke test runner for PCS generated code
# Run with: julia --project -e 'include("examples/julia/run_simple.jl"); @show PCS_Generated.main()'

# Simple test case: sum of squares of even numbers
module PCS_Generated

function main()::Int
    acc1 = 0
    for x in 1:99
        if (x % 2 == 0)
            acc1 += x * x
        end
    end
    return acc1
end

end # module

# Test the generated function
println("Testing PCS generated Julia code...")
result = PCS_Generated.main()
println("Result: ", result)
println("Expected: ", sum(x*x for x in 1:99 if x % 2 == 0))
println("Test passed: ", result == sum(x*x for x in 1:99 if x % 2 == 0))
