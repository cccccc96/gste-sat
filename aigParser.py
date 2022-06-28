import aiger
from aiger.aig import *
from pysmt.shortcuts import *
from dualEncoding import *



def parseAiger(filename):
    # example:'./example/memory1x1.aag'
    aig = aiger.load(filename)

    latch_map = dict(aig.latch_map)
    boundary = set(aig.node_map.values()) | set(latch_map.values())

    store, prev, mem = {}, set(), {}
    for node_batch in aig.__iter_nodes__():
        for gate in node_batch:
            if isinstance(gate, Inverter):
                mem[gate] = ~ mem[gate.input]
            elif isinstance(gate, AndGate):
                mem[gate] = mem[gate.left] & mem[gate.right]
            elif isinstance(gate, Input):
                mem[gate] = DualSymbol(Symbol(gate.name+"Left"),Symbol(gate.name+"Right"))
            elif isinstance(gate, LatchIn):
                # BOOL变量 (nameLeft,nameRight)
                mem[gate] = DualSymbol(Symbol(gate.name+"Left"),Symbol(gate.name+"Right"))
            elif isinstance(gate, ConstFalse):
                mem[gate] = DualSymbol(FALSE(),TRUE())
            if gate in boundary:
                store[gate] = mem[gate]
    out_map = {out: store[gate] for out, gate in aig.node_map.items()}
    # louts = {out: store[gate] for out, gate in latch_map.items()}

    outs = out_map
    louts = {}
    for out,gate in latch_map.items():
        if out not in out_map:
            louts[out] = store[gate]


    return outs,louts,aig.inputs
