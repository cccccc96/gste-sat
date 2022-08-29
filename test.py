from z3 import *
a = BitVec('a',2)
b = BitVec('b',2)
val_3 = BitVecVal(1,2)
val_3_ = BitVecVal(3,2)
x = simplify(val_3_+val_3_)
print(x)


