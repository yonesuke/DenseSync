import logging
import math
import os

import functions as F
import hydra
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.size"] = 20


@hydra.main(config_name="config")
def plot_sup_m(cfg):
    max_N = cfg.sup_m.max_N

    Kc = F.binary_search(f=F.t, xl=0.335, xr=0.345, eps=1e-8)

    ns = [i for i in range(7, max_N + 1)]
    ss = [F.sup_m(n) for n in ns]

    plt.figure(figsize=[8, 6])
    plt.xlim(7, max_N)
    plt.xlabel("$\widetilde{N}$")
    plt.ylabel(r"$\alpha_{\widetilde{N}}/\widetilde{N}$")
    plt.plot(
        [7, max_N],
        [ss[12], ss[12]],
        color="gray",
        linestyle="dashed",
        label=r"New lower bound of $\mu_{c}$",
        zorder=10,
    )
    plt.plot(
        [7, max_N],
        [1277 / 1870, 1277 / 1870],
        color="gray",
        linestyle="dotted",
        label=r"Previous lower bound of $\mu_{c}$",
        zorder=10,
    )
    plt.plot([7, max_N], [2 * Kc, 2 * Kc], color="red", label=r"$2K_{c}$", zorder=0)
    plt.scatter(ns, ss, s=10, zorder=10)
    plt.legend(loc="lower right")
    plt.tight_layout()

    current_dir = hydra.utils.get_original_cwd()
    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    os.makedirs(fig_dir, exist_ok=True)
    path = os.path.join(fig_dir, "sup_m.png")
    plt.savefig(path, bbox_inches="tight")

    logging.info(f"Save the figure {path}")


if __name__ == "__main__":
    plot_sup_m()
