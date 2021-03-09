import os
import hydra
import logging
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc('text', usetex=True)
plt.rcParams["font.size"] = 20


@hydra.main(config_name="config")
def plot(cfg):
    current_dir = hydra.utils.get_original_cwd()
    result_dir = os.path.join(current_dir, cfg.hp.result_dir)

    df = pd.read_csv(os.path.join(result_dir, 'results.csv'), header=0)
    pre_lower_bound = 1277 / 1870
    
    fig, ax = plt.subplots(figsize=(12, 8))

    # df.plot.scatter('N', 'r', c='p', colormap='viridis', ax=ax, s=6)
    df.plot.scatter('N', 'r', ax=ax, s=8)

    ax.plot([0, df['N'].max()], [pre_lower_bound, pre_lower_bound], linestyle="dashed", color="gray", label=r'Previous lower bound of $\mu_c$')

    ax.set_ylim([0.62, 0.687])
    ax.set_xlim([5, df['N'].max()])
    ax.set_xlabel(r'$N$')
    ax.set_ylabel(r'$\max_{1\leq p \leq \lfloor N/2 \rfloor \\}{\mu^{(N, p)}}$')
    ax.legend(bbox_to_anchor=(1, 0), loc='lower right', borderaxespad=1)


    fig_dir = os.path.join(current_dir, cfg.hp.fig_dir)
    path = os.path.join(fig_dir, "figure1.png")

    os.makedirs(fig_dir, exist_ok=True)
    plt.savefig(path, bbox_inches='tight')

    logging.info(f"Save the figure {path}")


if __name__ == '__main__':
    plot()