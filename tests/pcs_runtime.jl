# pcs_runtime.jl — zero-deps helpers for PCS-generated Julia code
module PCS_Runtime
using Base.Threads
import Base.Threads: @threads, nthreads, threadid

export parallel_reduce_parts!, combine_parts, merge_shards!, dict_comp_parallel, groupby_parallel, unsafe_wrap, finalize_groups!

# Unsafe optimizations toggle
const USE_UNSAFE = Ref(false)

# Helper to conditionally wrap with unsafe optimizations
unsafe_wrap(s) = USE_UNSAFE[] ? s : ""

# Thread-local partials for associative reductions
function parallel_reduce_parts!(parts, range_iter, f, pred)
    @threads for i in range_iter
        x = f(i)  # caller chooses map f, or identity
        if pred(i, x)
            @inbounds parts[threadid()] += x
        end
    end
    return parts
end

# Combine thread-local partials
combine_parts(parts; init=0) = (acc = init; @inbounds for p in parts; acc += p; end; acc)

# Merge a shard Dict into dst using a combining function (last-write wins by default)
function merge_shards!(dst::Dict{K,V}, shard::Dict{K,V}, combine = (old,new)->new) where {K,V}
    @inbounds for (k, v) in shard
        dst[k] = haskey(dst, k) ? combine(dst[k], v) : v
    end
    return dst
end

# Parallel dict-comp via per-thread shards + serial merge
function dict_comp_parallel(range_iter, key::Function, val::Function;
                            KT::Type=Int, VT::Type=Int, combine = (old,new)->new)
    shards = [Dict{KT,VT}() for _ in 1:nthreads()]
    @threads for i in range_iter
        k = key(i); v = val(i)
        sh = shards[threadid()]
        sh[k] = haskey(sh, k) ? combine(sh[k], v) : v
    end
    out = Dict{KT,VT}()
    @inbounds for sh in shards
        merge_shards!(out, sh, combine)
    end
    return out
end

# Parallel group-by via per-thread shards + serial merge
function groupby_parallel(xs; key::Function, KT::Type=Int, T::Type=Any)
    shards = [Dict{KT, Vector{T}}() for _ in 1:nthreads()]
    @threads for i in eachindex(xs)
        x = xs[i]; k = key(x)
        v = get!(shards[threadid()], k, Vector{T}())
        push!(v, x)
    end
    out = Dict{KT, Vector{T}}()
    @inbounds for sh in shards
        for (k, v) in sh
            dst = get!(out, k, Vector{T}())
            append!(dst, v)
        end
    end
    return out
end

# Group-by stable ordering option
function finalize_groups!(d::Dict; stable::Bool=false)
    if stable
        for (k, v) in d
            # Stable by second field example (customize as needed)
            if length(v) > 1 && eltype(v) <: Tuple
                sort!(v, by = x -> x[2]) 
            end
        end
    end
    return d
end

end # module
