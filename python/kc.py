import os
import math
import hydra
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('text', usetex=True)


def t(x):
    return 4*np.pi*x-4*np.sin(2*np.pi*x)+np.sin(4*np.pi*x)


def f(x):
    return -np.cos(x)*(1-np.cos(x))


def critical_index(N):
    xs = np.array([2*np.pi*l/N for l in range(1,N)])
    ys = f(xs)
    sk = np.cumsum(ys)
    kc = np.argmax(sk>=0) + 1
    return kc


@hydra.main()
def plot_kc(cfg):
    current_dir = hydra.utils.get_original_cwd()

    max_N=100
    eps = 10**(-8)
    xl, xr = 0.335, 0.345
    while (xr-xl)>eps:
        xm = (xl + xr) * 0.5
        if t(xm)>0:
            xr = xm
        else:
            xl = xm
    Kc = xl


    a = (1/6+np.sqrt(3)/4)*np.pi

    ns = np.array([i for i in range(7, max_N+1)])
    kcs = np.array([critical_index(n)/n for n in ns])
    maxs = np.array([Kc+0.5/n+a/n/n for n in ns])
    sups = np.array([np.ceil(Kc*n-0.5+a/n)/n for n in ns])


    plt.figure(figsize=(8,6))
    plt.rcParams['font.size']=20
    plt.xlim(7,max_N)
    plt.xlabel(r"$\widetilde{N}$")
    plt.ylabel(r"$k_{\mathrm{c}}/\widetilde{N}$")
    plt.scatter(ns,kcs,s=10,zorder=10)
    plt.plot(ns,maxs,color="gray",linestyle="dashed",label=r"$K_{\mathrm{c}}+1/(2\widetilde{N})+2\pi/(3\widetilde{N}^{2})$",zorder=10)
    plt.plot(ns,sups,color="gray",linestyle="dotted",label=r"$\lceil K_{\mathrm{c}}\widetilde{N}-1/2+2\pi/(3\widetilde{N})\rceil/\widetilde{N}$",zorder=10)
    plt.plot([7,max_N],[Kc,Kc],color="red",label=r"$K_{\mathrm{c}}$",zorder=0)
    plt.legend(loc="upper right")
    plt.tight_layout()

    os.makedirs(os.path.join(current_dir, "figs"), exist_ok=True)
    plt.savefig(os.path.join(current_dir, "figs", "kc.png"), bbox_inches='tight')


if __name__ == '__main__':
    plot_kc()