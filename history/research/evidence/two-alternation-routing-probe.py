"""Finite exact-distance tests of guarded hypercube routing configurations."""
from itertools import combinations
import json


def ball(center, radius, dimension):
    return {center ^ sum(1<<i for i in bits)
            for size in range(radius+1) for bits in combinations(range(dimension),size)}


def build(d, targets, k, guard=True):
    r=d
    block=2*d+3
    dimension=4*block+d
    masks=[((1<<block)-1)<<(d+i*block) for i in range(4)]
    o,s,g,h=masks
    moon=set(range(1<<d))
    near_moon=moon | {v^(1<<i) for v in moon for i in range(dimension)}
    surface=sorted(ball(o,r,dimension)-ball(o,r-1,dimension))
    slots=surface[:k]
    forced_vertices=(near_moon | ball(o,r+1,dimension))-set(targets)-set(slots)
    forced=[(v,v^h) for v in sorted(forced_vertices-{o})]+[(o,s)]
    if guard:
        forced += [(v,v^g) for v in sorted(ball(s,r,dimension)-{s})]
    endpoints=[v for edge in forced for v in edge]
    assert len(endpoints)==len(set(endpoints))
    assert not set(endpoints)&(set(targets)|set(slots))
    assert all((u^v).bit_count()>1 for u,v in forced)
    if guard:
        assert ball(s,r,dimension)<=set(endpoints)
    alpha=len(targets)*(r+2)+1
    bound=alpha*len(forced)+len(targets)*(2*r+3)-2*k
    return dimension,o,s,slots,forced,alpha,bound


def distance2(u,v,edges):
    best=2*(u^v).bit_count()
    mates={}
    for a,b in edges:
        assert a not in mates and b not in mates
        mates[a]=b; mates[b]=a
        best=min(best,2*((u^a).bit_count()+(b^v).bit_count())+1,
                 2*((u^b).bit_count()+(a^v).bit_count())+1)
    if u in mates and v in mates:
        best=min(best,2+2*(mates[u]^mates[v]).bit_count())
    return best


def dominates(targets, selected):
    return all(any((u^v).bit_count()<=1 for v in selected) for u in targets)


sources=configurations=demand_checks=feasible=0
geometry=[]
for d in (1,2):
    vertices=list(range(1<<d))
    for size in range(1,len(vertices)+1):
        for targets in combinations(vertices,size):
            for k in range(1,size+1):
                dimension,o,s,slots,forced,alpha,bound=build(d,targets,k)
                sources+=1
                geometry.append(len(forced))
                for selected in combinations(targets,k):
                    edges=forced+list(zip(selected,slots))
                    low=[distance2(t,o,edges) for t in targets]
                    total=alpha*len(forced)+sum(low)
                    assert all(cost>=2*d+1 for cost in low)
                    assert sum(cost==2*d+1 for cost in low)==k
                    assert (total<=bound)==dominates(targets,selected)
                    configurations+=1; demand_checks+=len(targets); feasible+=total<=bound

d=2; targets=(0,3); k=1
dimension,o,s,slots,forced,alpha,bound=build(d,targets,k,guard=False)
occupied={v for edge in forced for v in edge}|set(targets)|set(slots)
shortcut=next(s^(1<<i) for i in range(dimension) if s^(1<<i) not in occupied)
edges=forced+[(0,slots[0]),(3,shortcut)]
low=[distance2(t,o,edges) for t in targets]
assert not dominates(targets,(0,))
assert alpha*len(forced)+sum(low)<=bound
print(json.dumps({'source_cases':sources,'configurations':configurations,
    'low_demand_distance_checks':demand_checks,'feasible_configurations':feasible,
    'forced_edges_min':min(geometry),'forced_edges_max':max(geometry),
    'unguarded_counterexample':{'dimension':dimension,'targets':targets,'k':k,
    'selected':0,'extra_edge':[3,shortcut],'scaled_low_costs':low,
    'scaled_low_budget':len(targets)*(2*d+3)-2*k}},indent=2))
