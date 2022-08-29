from aigParser import *
from util import *
from trajFormula import *

filename = './example/rbFIFO-1-3-1.aag'
transitionSystem = parseAiger(filename)
t = PLUSN('head',3)
print(t.sumList())

y = READ('mem','head')
y2 = y.idxNameToInt('head')
y3 = y.eleList()
for item in y3:
    print(item)
solve(y2==2)
print(y2)

print(1)
