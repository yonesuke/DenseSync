import logging
import math
import os

import functions as F
import hydra
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.size"] = 28


@hydra.main(config_name="config")
def plot(cfg):
    m = 3
    nt = 60
    N, p = nt * m, m

    plt.figure(figsize=[20, 6])

    _xs = np.arange(0, m * 2 * np.pi, 0.01)
    _ys = F.b(_xs)
    # plt.plot(_xs, _ys, label=r"$-\cos\theta+\cos^{2}\theta$", color="gray", linewidth=1, zorder=1)
    plt.plot(_xs, _ys, color="gray", linewidth=1, zorder=1)
    plt.plot([0, m * 2 * np.pi], [0, 0], linestyle="dashed", color="gray", zorder=0)

    kc, ys, sk = F.critical_index(nt)
    colors = ["white" for _ in range(1, N)]

    # kcまでを塗る
    for i in range(m):
        for j in range(kc - 1):
            colors[i * nt + j] = "tab:blue"
            colors[i * nt + nt - kc + j] = "tab:blue"

    # ntの上を塗る
    for i in range(1, m):
        colors[i * nt - 1] = "tab:orange"

    # 追加で塗る
    # (N,p)=(60*3,3)のとき追加で4つ塗る
    colors[kc - 1] = "tab:pink"
    colors[N - kc - 1] = "tab:pink"
    colors[nt - kc - 1] = "tab:pink"
    colors[N - nt + kc - 1] = "tab:pink"

    xs = [2 * np.pi * l / nt for l in range(1, N)]
    ys = F.b(xs)
    plt.scatter(xs, ys, zorder=10, color=colors, edgecolors="tab:gray", linewidths=0.3)

    plt.xlim(0, m * 2 * np.pi)
    plt.xlabel(r"$2{\pi}pl/N$")
    plt.ylabel(r"$b^{(N,p)}_{l}$")
    xlocs = [
        0,
        0.5 * np.pi,
        np.pi,
        1.5 * np.pi,
        2 * np.pi,
        2.5 * np.pi,
        3 * np.pi,
        3.5 * np.pi,
        4 * np.pi,
        4.5 * np.pi,
        5 * np.pi,
        5.5 * np.pi,
        6 * np.pi,
    ]
    xlabs = [
        "$0$",
        r"$\frac{\pi}{2}$",
        r"$\pi$",
        r"$\frac{3\pi}{2}$",
        r"$2\pi$",
        r"$\frac{5\pi}{2}$",
        r"$3\pi$",
        r"$\frac{7\pi}{2}$",
        r"$4\pi$",
        r"$\frac{9\pi}{2}$",
        r"$5\pi$",
        r"$\frac{11\pi}{2}$",
        r"$6\pi$",
    ]
    plt.xticks(xlocs, xlabs)
    plt.tight_layout()

    current_dir = hydra.utils.get_original_cwd()
    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    os.makedirs(fig_dir, exist_ok=True)

    path = os.path.join(fig_dir, "N180p3.png")
    plt.savefig(path)

    logging.info(f"Save the figure {path}")


if __name__ == "__main__":
    plot()
