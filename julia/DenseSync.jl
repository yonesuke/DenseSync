using JuMP
using Cbc

struct DenseSync
    N::Int64
    p::Int64
    μ::Rational
    x::Array
end

Base.show(io::IO, ds::DenseSync) = print(io, "DenseSync{\n system size: ", ds.N, ", p-twisted state: ", ds.p, ", \n μ = ", ds.μ, " ≃ ", float(ds.μ), "\n x = ", ds.x, "\n}")

function max_connectivity(N::Int64, p::Int64, ε = 10^(-5), limit_sec = 60)
    function L_kl(k, l)
        return cos(2π*p*l/N)*(-1+cos(2*π*k*l/N))
    end
    L = [L_kl(k,l) for k in 1:N-1, l in 1:N-1]
    # model
    model = Model(Cbc.Optimizer)
    set_time_limit_sec(model, limit_sec)
    set_silent(model)
    # variable
    @variable(model, x[i=1:N-1], Bin)
    # maximizing function
    ex = @expression(model, sum(x))
    @objective(model, Max, ex)
    # constraint
    @constraint(model, L*x .≤ -ε) # negative eigenvalues
    @constraint(model, [i=1:(N-1)÷2], x[i]==x[N-i]) # undirected constraint
    # solve!!
    optimize!(model)
    if termination_status(model) == MOI.OPTIMAL
        μ = objective_value(model)
        μ = Int(μ)//(N-1)
        ans = [Int(round(a)) for a in value.(x)]
        time = solve_time(model)
        @info "maximum connectivity obtained by direct optimization" N p μ=string(μ, " ≃ ",round(μ, digits=7)) time=string(round(time, digits=3), "[s]")
        return DenseSync(N, p, μ, ans)
    else
        μ = -1
        @info "maximum connectivity obtained by direct optimization" N p μ
        return DenseSync(N, p, μ, zeros(Int, N-1))
    end
end

function exact_sol(N::Int64, p::Int64)
    @assert gcd(N,p)==p
    m = p
    n = N ÷ m
    @assert n ≥ 5
    b(x) = -cos(x)*(1-cos(x))
    # compute critical index kc and number of indecies additonally set to one
    kc, add = begin
        xs = [2π*l/n for l in 1:n-1]
        ys = b.(xs)
        sk = cumsum(ys)
        critical_index = findfirst(x -> x ≥ 0, sk)
        additioal = 2*Int(ceil(-m*sk[critical_index-1]/(sk[critical_index]-sk[critical_index-1])-1))
        critical_index, additioal
    end
    # calcilate maximum connectivity
    connects = 2*m*(kc-1) + m-1 + additioal
    μ = connects//(N-1)
    # next, we obtain optimal solution
    x = zeros(Int, N-1)
    # step 1
    for i in 1:m
        for j in 1:kc-1
            x[(i-1)*n + j] = 1
            x[i*n - kc + j] = 1
        end
    end
    # step 2
    for i in 1:m-1
        x[i*n] = 1
    end
    # step 3
    candidates = Int[]
    for i in 1:m
        append!(candidates, (i-1)*n+kc)
        append!(candidates, i*n-kc)
    end
    for i in 1:add÷2
        x[candidates[i]] = 1
        x[N-candidates[i]] = 1
    end
    @info "maximum connectivity obtained by Theorem 1" N p μ=string(μ, " ≃ ",round(μ, digits=7))
    return DenseSync(N, p, μ, x)
end
