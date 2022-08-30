from z3 import *



class SORT:
    sort_map = {}
    pass

class BOOLEAN(SORT):
    # origin boolean sort label of node name
    pass

class BITVEC(SORT):
    # origin bitvec sort label of node name
    # eg: "head":BITVEC(i)
    #       represents in aig "head" will be blasted to head[0] ,..., head[i-1]
    def __init__(self,length):
        self.length = length

class ARRAY(SORT):
    # origin array sort label of node name
    # eg: "mem":array(i,j)
    #       represents in aig "mem" will be blasted to mem[0][0] ,..., mem[i-1][j-1]
    def __init__(self,idx_len, ele_len):
        self.idx_len = idx_len
        self.ele_len = ele_len


def is_sat(f):
    solver = Solver()
    solver.add(f)
    if solver.check() == sat:
        # print(solver.model())
        return True
    else:
        return False

def next_var(v):
    """Returns the 'next' of the given variable"""
    name = str(v)
    return Bool("%s_" % name)


def at_time(v, t):
    """Builds an SMT variable representing v at time t"""
    name = str(v)
    return Bool("%s@%d" % (name, t))


class TransitionSystem(object):
    def __init__(self, variables, trans, regs):
        self.variables = variables
        self.trans = trans
        self.regs = regs
