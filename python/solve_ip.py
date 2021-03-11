import os
import math
import pulp
import logging
import hydra
import numpy as np

logging.basicConfig(level=logging.INFO)


def solve(N, p, eps=1e-5):
    """ solve an integer programming problem for finding a circulant network with maximum connectivity

    Parameters
    ----------
    N : int
      The number of oscillators
    p : int
      p-twisted state

    Returns
    -------
    result: float
      An objective value after solving
    a: 
      a base after solving
    """

    problem = pulp.LpProblem('GraphSync', pulp.LpMaximize)
    a = pulp.LpVariable.dicts('a', (range(1, N)), cat = pulp.LpBinary)
    
    # define connectivity as objective function
    problem += 1.0/(N-1) * pulp.lpSum(a[i] for i in range(1, N))
    
    # eigenvalue constraint
    for r in range(1, N):
        problem += (pulp.lpSum(a[s]*np.cos(p*2.0*np.pi*s/N)*(-1.0+np.cos(r*2.0*np.pi*s/N)) for s in range(1, N)) <= -eps)

    # symmetric constraint
    for i in range(1, int(np.floor((N+1)/2))):
        problem += (a[i] == a[N-i])

    status = problem.solve(pulp.PULP_CBC_CMD(threads=8, msg=0, timeLimit=60))
    result = pulp.value(problem.objective)
    
    return result, a


@hydra.main(config_name="config")
def search(cfg):
    current_dir = hydra.utils.get_original_cwd()
    result_dir = os.path.join(current_dir, cfg.hp.result_dir)
    os.makedirs(os.path.join(result_dir, "base"), exist_ok=True)

    csv_path = os.path.join(result_dir, f'results.csv')
    with open(csv_path, 'w') as f:
        f.write(f'N,p,r\n')

    for N in range(2, cfg.hp.max_N + 1):
        for p in range(1, math.floor(N/2)):
            r, a = solve(N, p)
            logging.info(f"N={N},\tp={p},\tmax_connectivity={r:.3}")

            with open(csv_path, 'a') as f:
                f.write(f'{N},{p},{r}\n')
            
            #with open(os.path.join(result_dir, "base", f'N={N}_p={p}'), 'w') as f:
            #    for i in range(1, N):
            #        f.write(f'{int(a[i].value())} ')
            #    f.write('\n')


if __name__ == '__main__':
    search()
