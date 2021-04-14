include("DenseSync.jl")
using FFTW
using LinearAlgebra
using Plots
gr()

function rungekutta(func, θ0, δt, tmax, rec_func)
    ans = []
    for _ in 1:tmax÷δt
        k1 = func(θ0)
        k2 = func(θ0 + 0.5*δt*k1)
        k3 = func(θ0 + 0.5*δt*k2)
        k4 = func(θ0 + δt*k3)
        θ0 += δt*(k1 + 2k2 + 2k3 + k4)/6.0
        append!(ans, rec_func(θ0))
    end
    return ans
end
    
function DenseSyncODE(ds::DenseSync, δt, tmax)
    x = append!([0], copy(ds.x))
    y = fft(x)
    function ODEVec(θs)
        es = exp.(1im*θs)
        return imag.(conj.(es).*(ifft(y.*fft(es))))
    end
    N = ds.N
    θ_twisted = [2π*l*ds.p/N for l in 0:N-1]
    function TwistedNorm(θs)
        vec = mod2pi.(θs - θ_twisted)
        vec = [(x≥π ? 2π-x : x) for x in vec]
        return norm(vec)
    end
    # initial value
    σ = 0.1π
    noises = σ*randn(N)/√(N)
    noises = noises .- sum(noises)/N
    θ0 = θ_twisted + noises
    return rungekutta(ODEVec, θ0, δt, tmax, TwistedNorm)
end

N, p = 1900, 100
ds = exact_sol(N, p)

δt, tmax = 10^(-3), 4
ts = [i*δt for i in 1:tmax÷δt]
norms = [DenseSyncODE(ds, δt, tmax) for _ in 1:5]
plot(
    ts, [log.(norm) for norm in norms],
    xlims=(0, 4), label=false,
    xlabel="t", ylabel="log norm"
)
savefig("ode.png")
