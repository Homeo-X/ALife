from concurrent.futures import ProcessPoolExecutor
from statistics import mean, pstdev
from omega.experiments.registry import get_experiment
from omega.experiments.harness import run
SEEDS=list(range(5))
def one(a):
    ps, arm, seed = a
    mode = 'mixed' if arm=='mixed' else 'source'
    fit = 'size' if arm=='source-size' else 'network'
    p,c=get_experiment('exp022')(seed=seed,ticks=4000,n_patches=24,propagule_mode=mode,
        propagule_size=ps, deme_fitness=fit, measure_xprod=True)
    r=run(p,c); g=[m['gauges'].get('mean_cross_prod',0) for m in r.metrics]
    return (ps,arm,mean(g[-len(g)//4:]) if g else 0)
jobs=[(ps,arm,s) for ps in (16,24) for arm in ('source-network','source-size','mixed') for s in SEEDS]
with ProcessPoolExecutor(max_workers=8) as ex: rows=list(ex.map(one,jobs))
print(f"{'psize':>5s} {'source-network':>15s} {'source-size':>13s} {'mixed':>10s}")
for ps in (16,24):
    def m(arm):
        v=[r[2] for r in rows if r[0]==ps and r[1]==arm]; return f"{mean(v):.2f}±{pstdev(v):.2f}"
    print(f"{ps:5d} {m('source-network'):>15s} {m('source-size'):>13s} {m('mixed'):>10s}")
