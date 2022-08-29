import aiger
from aiger.aig import *
from util import *
import re


def parseAiger(filename):
    # example:'./example/memory1x1.aag'
    aig = aiger.load(filename)

    latch_map = dict(aig.latch_map)
    boundary = set(aig.node_map.values()) | set(latch_map.values())

    store, prev, mem = {}, set(), {}
    for node_batch in aig.__iter_nodes__():
        for gate in node_batch:
            if isinstance(gate, Inverter):
                mem[gate] = Not(mem[gate.input])
            elif isinstance(gate, AndGate):
                mem[gate] = And(mem[gate.left] , mem[gate.right])
            elif isinstance(gate, Input):
                mem[gate] = Bool(gate.name)
            elif isinstance(gate, LatchIn):
                # BOOL变量 (nameLeft,nameRight)
                mem[gate] = Bool(gate.name)
            elif isinstance(gate, ConstFalse):
                mem[gate] = False
            else:
                assert "aigParser"
            if gate in boundary:
                store[gate] = mem[gate]

    l_map = {out: store[gate] for out, gate in latch_map.items()} #latch
    out_map = {out: store[gate] for out, gate in aig.node_map.items()} #out

    variables = []
    for input_signal_name in aig.inputs:
        variables.append(Bool(input_signal_name))
    for out_signal_name, gate in latch_map.items():
        variables.append(Bool(out_signal_name))
    for latch_singal_name, gate in latch_map.items():
        variables.append(Bool(latch_singal_name))

    for variable in variables:
        variable_name = str(variable)
        if variable_name.count('[') == 0:
            name = variable_name
            SORT.sort_map[name] = BOOLEAN()
        elif variable_name.count('[') ==1:
            matchObj = re.match(r"(.*)\[([^\[\]]*)\](.*)",variable_name,re.I|re.M)
            name = matchObj.group(1)
            length = int(matchObj.group(2))+1
            length_ = SORT.sort_map[name].length if name in SORT.sort_map else -1
            if length>length_:
                SORT.sort_map[name] = BITVEC(length)
        elif variable_name.count('[') ==2:
            matchObj = re.match(r"(.*)\[([^\[\]]*)\]\[([^\[\]]*)\](.*)",variable_name,re.I|re.M)
            name = matchObj.group(1)
            idx_len = int(matchObj.group(2))+1
            ele_len = int(matchObj.group(3))+1
            idx_len_ = SORT.sort_map[name].idx_len if name in SORT.sort_map else -1
            ele_len_ = SORT.sort_map[name].ele_len if name in SORT.sort_map else -1
            if idx_len>idx_len_ and ele_len>ele_len_:
                SORT.sort_map[name] = ARRAY(idx_len,ele_len)
            elif idx_len>idx_len_ :
                SORT.sort_map[name] = ARRAY(idx_len, ele_len_)
            elif ele_len>ele_len_ :
                SORT.sort_map[name] = ARRAY(idx_len_, ele_len)

    trans_list = []
    for latch_name,formula in l_map.items():
        tran = next_var(Bool(latch_name)) == formula
        trans_list.append(tran)
    for out_name,formula in out_map.items():
        tran = next_var(Bool(out_name)) == formula
        trans_list.append(tran)
    trans = And(trans_list)

    return TransitionSystem(variables,trans)






