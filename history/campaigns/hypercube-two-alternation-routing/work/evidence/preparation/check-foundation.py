from pathlib import Path
import importlib.util
import json

work=Path(__file__).resolve().parents[2]
def load(name):
    spec=importlib.util.spec_from_file_location(name,work/(name+'.py'))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
check=load('check')
verify=load('verify')
comparisons=0
for dimension in (1,2):
    for bound in range(9):
        target={'cube':'1'*dimension,'demands':[[0,(1<<dimension)-1,2],[1,0,1]],'bound':bound}
        expected=any(check.target_witness(target,m) for m in check.matchings(list(range(1<<dimension))))
        witness,_=verify.solve(target)
        assert (witness is not None)==expected
        comparisons+=1
for bound, expected in ((23, False), (24, True)):
    target={'cube':'1111','demands':[[0,3,10],[15,7,10],[0,15,1]],'bound':bound}
    assert (check.target_solve(target) is not None)==expected
    assert (verify.solve(target)[0] is not None)==expected
source={'dimension':1,'active':[1,1],'k':1}
fixture=Path(__file__).with_name('wrong-map-fixture.py')
wrong_target=check.invoke(fixture,source)
assert check.source_solve(source) is not None and check.target_solve(wrong_target) is None
wrong_recovery=check.invoke(fixture,{'source':source,'target_solution':[]},True)
assert not check.source_witness(source,wrong_recovery)
print(json.dumps({'route_enumerator_exhaustive_crosschecks':comparisons,'strict_two_dynamic_edge_cases':2,'wrong_forward_detected':True,'wrong_recovery_detected':True}))
