import json
import sys
print(json.dumps([] if '--extract' in sys.argv else {'cube':'1','demands':[[0,1,1]],'bound':0}))
