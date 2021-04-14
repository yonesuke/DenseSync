## Experiments

### Figure 1

[`solve_ip.py`](solve_ip.py) and [`solve_ip_multi.py`](solve_ip_multi.py) are solving an integer programming problem (Problem 1 in the paper).

You need to execute either one.

+ single processing ver.

    ```
    python solve_ip.py -m hp.max_N=600
    ```

+ multi processing ver.

    This program is faster than single processing ver.

    ```
    python solve_ip_multi.py -m hp.max_N=600
    ```


After the execution, the maximum connectivity for each N and p is saved as `./results/results.csv`.
The graph of the maximum connectivity and the number of oscillators is plotted by the below command.

```
python max_connectivity.py
```

![](figs/figure1.png)

### Figure 2

```
python n60p1.py
```

![](figs/N60p1.png)

### Figure 3

```
python n180p3.py
```

![](figs/N180p3.png)

### Figure 4

```
python sup_m.py
```

![](figs/sup_m.png)

### Figure 5

```
python odeplot.py -m ode_plot.N=1900 ode_plot.p=100
```

![](figs/ode.png)

### Figure 6

```
python kc.py
```

![](figs/kc.png)