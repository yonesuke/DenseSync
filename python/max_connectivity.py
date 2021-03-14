import os
import hydra
import logging
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 16

@hydra.main(config_name="config")
def plot(cfg):
    current_dir = hydra.utils.get_original_cwd()
    result_dir = os.path.join(current_dir, cfg.hp.result_dir)

    pre_lower_bound = 1277 / 1870
    Nmin, Nmax = 30, 600
    df = pd.read_csv(os.path.join(result_dir, 'results.csv'), header=0)
    
    fig, ax = plt.subplots(figsize=(8, 6))

    df = df[(df['N'] >= Nmin) & (df['N'] <= Nmax)]
    max_m = df.groupby('N', as_index=False).max()
    max_m.plot.scatter('N', 'r', ax=ax, s=10, zorder=10)

    ax.plot([0, df['N'].max()], [pre_lower_bound, pre_lower_bound], linestyle="dashed", color="gray", label=r'Previous lower bound of $\mu_c$')

    ax.set_xlim([Nmin-1, Nmax+1])
    ax.set_ylim([0.622, 0.685])
    ax.set_xlabel(r'$N$')
    ax.set_ylabel(r'$\max_{1\leq p\leq \lfloor N/2\rfloor} \mu^{(N,p)}$')

    ax.legend(loc='lower right')
    fig.tight_layout()

    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    path = os.path.join(fig_dir, "figure1.png")

    os.makedirs(fig_dir, exist_ok=True)
    plt.savefig(path, bbox_inches='tight')

    logging.info(f"Save the figure {path}")


if __name__ == '__main__':
    plot()