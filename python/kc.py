import logging
import math
import os

import functions as F
import hydra
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


@hydra.main(config_name="config")
def plot_kc(cfg):
    max_N = 100
    eps = 10 ** (-8)
    xl, xr = 0.335, 0.345
    while (xr - xl) > eps:
        xm = (xl + xr) * 0.5
        if F.t(xm) > 0:
            xr = xm
        else:
            xl = xm
    Kc = xl

    a = (1 / 6 + np.sqrt(3) / 4) * np.pi

    ns = np.array([i for i in range(7, max_N + 1)])
    kcs = np.array([F.critical_index(n) / n for n in ns])
    maxs = np.array([Kc + 0.5 / n + a / n / n for n in ns])
    sups = np.array([np.ceil(Kc * n - 0.5 + a / n) / n for n in ns])

    plt.figure(figsize=(8, 6))
    plt.rcParams["font.size"] = 20
    plt.xlim(7, max_N)
    plt.xlabel(r"$\widetilde{N}$")
    plt.ylabel(r"$k_{\mathrm{c}}/\widetilde{N}$")
    plt.scatter(ns, kcs, s=10, zorder=10)
    plt.plot(
        ns,
        maxs,
        color="gray",
        linestyle="dashed",
        label=r"$K_{\mathrm{c}}+1/(2\widetilde{N})+2\pi/(3\widetilde{N}^{2})$",
        zorder=10,
    )
    plt.plot(
        ns,
        sups,
        color="gray",
        linestyle="dotted",
        label=r"${\lceil}K_{\mathrm{c}}\widetilde{N}-1/2+2\pi/(3\widetilde{N}){\rceil}/\widetilde{N}$",
        zorder=10,
    )
    plt.plot([7, max_N], [Kc, Kc], color="red", label=r"$K_{\mathrm{c}}$", zorder=0)
    plt.legend(loc="upper right")
    plt.tight_layout()

    current_dir = hydra.utils.get_original_cwd()
    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    path = os.path.join(fig_dir, "kc.png")

    os.makedirs(fig_dir, exist_ok=True)
    plt.savefig(path, bbox_inches="tight")

    logging.info(f"Save the figure {path}")


if __name__ == "__main__":
    plot_kc()
