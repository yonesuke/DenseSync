include("DenseSync.jl")

p = 16
for m in 1:15
    max_connectivity(m*p, m)
end
