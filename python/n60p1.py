import logging
import os

import functions as F
import hydra
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.size"] = 25


@hydra.main(config_name="config")
def plot(cfg):
    plt.figure(figsize=[8, 6])

    _xs = np.arange(0, 2 * np.pi, 0.01)
    _ys = F.b(_xs)
    # plt.plot(_xs, _ys, label=r"$-\cos\theta+\cos^{2}\theta$", color="gray", linewidth=1, zorder=1)
    plt.plot(_xs, _ys, color="gray", linewidth=1, zorder=1)
    plt.plot([0, 2 * np.pi], [0, 0], linestyle="dashed", color="gray", zorder=0)

    N = 60
    kc = 20
    colors = ["white" if kc <= i <= N - kc else "tab:blue" for i in range(1, N)]
    xs = [2 * np.pi * l / N for l in range(1, N)]
    ys = F.b(xs)
    plt.scatter(xs, ys, zorder=10, color=colors, edgecolors="tab:gray", linewidths=0.3)

    plt.xlim(0, 2 * np.pi)
    plt.xlabel(r"$2{\pi}pl/N$")
    plt.ylabel(r"$b^{(N,p)}_{l}$")
    xlocs = [0, 0.5 * np.pi, np.pi, 1.5 * np.pi, 2 * np.pi]
    xlabs = ["$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
    plt.xticks(xlocs, xlabs)
    # plt.legend(loc="upper right", frameon=False)
    plt.tight_layout()

    current_dir = hydra.utils.get_original_cwd()
    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    os.makedirs(fig_dir, exist_ok=True)

    path = os.path.join(fig_dir, "N60p1.png")
    plt.savefig(path)

    logging.info(f"Save the figure {path}")


if __name__ == "__main__":
    plot()
