import os
import hydra
import logging
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib

import functions as F

plt.rcParams['font.size'] = 20


def sup_m(N):
    xs = np.array([2*np.pi*l/N for l in range(1,N)])
    ys = F.b(xs)
    sk = np.cumsum(ys)
    kc = np.argmax(sk>=0) + 1
    return (2*kc-1-2*sk[kc-2]/ys[kc-1])/N


@hydra.main(config_name="config")
def plot_sup_m(cfg):
    max_N = 100
    eps = 10**(-8)
    xl, xr = 0.335, 0.345
    while (xr-xl)>eps:
        xm = (xl + xr) * 0.5
        if F.t(xm)>0:
            xr = xm
        else:
            xl = xm
    Kc = xl

    ns = [i for i in range(7,max_N+1)]
    ss = [sup_m(n) for n in ns]

    plt.figure(figsize=[8,6])
    plt.xlim(7,max_N)
    plt.xlabel("$\widetilde{N}$")
    plt.ylabel(r"$\alpha_{\widetilde{N}}/\widetilde{N}$")
    plt.plot([7,max_N],[ss[12],ss[12]],color="gray",linestyle="dashed",label=r"New lower bound of $\mu_{c}$",zorder=10)
    plt.plot([7,max_N],[1277/1870,1277/1870],color="gray",linestyle="dotted",label=r"Previous lower bound of $\mu_{c}$",zorder=10)
    plt.plot([7,max_N],[2*Kc, 2*Kc],color="red",label=r"$2K_{c}$",zorder=0)
    plt.scatter(ns,ss,s=10,zorder=10)
    plt.legend(loc="lower right")
    plt.tight_layout()

    current_dir = hydra.utils.get_original_cwd()
    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    os.makedirs(fig_dir, exist_ok=True)
    path = os.path.join(fig_dir, "sup_m.png")
    plt.savefig(path, bbox_inches='tight')

    logging.info(f"Save the figure {path}")


if __name__ == '__main__':
    plot_sup_m()