## Experiments

### Figure 1

[`solve_ip.py`](solve_ip.py) and [`solve_ip_multi.py](solve_ip_multi.py) are solving an integer programming problem (Problem 1 in the paper).
You need to execute either one.

#### 1. single processing ver.

```
python solve_ip.py -m hp.max_N=1000
```

#### 2. multi processing ver.

This program is faster than single processing ver.

```
python solve_ip_multi.py -m hp.max_N=1000
```


After the execution is finished, the result is saved as `./results/results.csv`.
The graph of the maximum connectivity and the number of oscillators `N` is plotted by below commnad.

```
python max_connectivity.py
```

### Figure 2

```
python n60p1.py
```

### Figure 3

```
python n180p3.py
```

### Figure 4

```
python sup_m.py
```

### Figure 5

```
python odeplot.py
```

### Figure 6

```
python kc.py
```