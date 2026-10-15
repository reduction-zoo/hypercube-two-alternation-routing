from pathlib import Path
import json
import subprocess
import sys
sys.set_int_max_str_digits(0)
p=Path(__file__).resolve().parents[2]/'algorithm.py'
no={'cube':'1','demands':[[0,1,1]],'bound':0}
objects=[None,[],{},True,{'dimension':True,'active':[1,1],'k':1},
         {'dimension':10**5000,'active':[1,1],'k':1},
         {'dimension':1,'active':[1,True],'k':1}]
for x in objects:
    r=subprocess.run([sys.executable,str(p)],input=json.dumps(x),text=True,capture_output=True,check=True)
    assert json.loads(r.stdout)==no
for raw in ('{','null null',''):
    r=subprocess.run([sys.executable,str(p)],input=raw,text=True,capture_output=True,check=True)
    assert json.loads(r.stdout)==no
x={'dimension':1,'active':[1,1],'k':10**5000}
r=subprocess.run([sys.executable,str(p)],input=json.dumps(x),text=True,capture_output=True,check=True)
assert json.loads(r.stdout)=={'cube':'1','demands':[],'bound':0}
r=subprocess.run([sys.executable,str(p),'--extract'],input=json.dumps({'source':x,'target_solution':[]}),text=True,capture_output=True,check=True)
assert json.loads(r.stdout)==[0,1]
print(json.dumps({'malformed_objects':len(objects),'malformed_json':3,'large_integer_forward_and_recovery':True}))
