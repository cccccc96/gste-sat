from aigParser import *
from TrajForm import *
from queue import Queue


def latchInit(louts):
    res = {}
    for latchName in louts:
        res[latchName] = DualSymbol(TRUE(), FALSE())
    return res

def stt_pred(antList,inputs):
    """ 计算antecedent

    :param antList:
    :return: example
        {
            'we':(TRUE,FALSE),
            'addr':(za,!za),
            ...
        }
    """
    res = {}
    for ant in antList:
        if isinstance(ant, isVar):
            res[ant.node] = DualSymbol(ant.value, Not(ant.value))
        elif isinstance(ant, guard):
            res[ant.node] = DualSymbol(Or(Not(ant.guard), ant.value), Or(Not(ant.guard), Not(ant.value)))
    for input in inputs:
        if input not in res:
            res[input] = DualSymbol(TRUE(),TRUE())
    return res


def post(antList, ckt_stt, outs, louts, inputs):
    fromTime = antList[0].fromTime

    if (fromTime-1,fromTime-1) in ckt_stt:
        fromTime = fromTime-1
        toTime = fromTime-1
    else:
        toTime = fromTime
        fromTime = fromTime-1

    res = {}

    # 计算subs {'name':DualSymbol()}
    subsLatch = {}
    # 上一时刻的ckt_stt
    for key, value in ckt_stt[(fromTime, toTime)].items():
        subsLatch[key] = value
    # 计算当前时刻latch的值
    for latchName, dualSymbol in louts.items():
        value = dualSymbol.substitute(subsLatch)
        res[latchName] = value

    subsOut = {}
    fromTime = antList[0].fromTime
    toTime = antList[0].toTime
    # 输入加入
    for ant in antList:
        if isinstance(ant, isVar):
            subsOut[ant.node] = DualSymbol(ant.value, Not(ant.value))
        elif isinstance(ant, guard):
            subsOut[ant.node] = DualSymbol(Or(Not(ant.guard), ant.value), Or(Not(ant.guard), Not(ant.value)))
    # 当前时刻的latch加入
    for latchName, dualSymbol in res.items():
        subsOut[latchName] = dualSymbol
    # 计算当前时刻的out的值
    for outName, dualSymbol in outs.items():
        value = dualSymbol.substitute(subsOut)
        res[outName] = value




    return res

def check(ckt_stt,consList):
    if consList == []:
        return True
    with Solver() as solver:
        fList = []
        for name,dualSymbol in ckt_stt.items():
            fList.append(EqualsOrIff(Symbol(name+"Left"),dualSymbol.left))
            fList.append(EqualsOrIff(Symbol(name + "Right"), dualSymbol.right))
        for cons in consList:
            if isinstance(cons, isVar):
                fList.append(EqualsOrIff(Symbol(cons.node+"Left"),cons.value))
                fList.append(EqualsOrIff(Symbol(cons.node + "Right"), Not(cons.value)))
            elif isinstance(cons, guard):
                fList.append(EqualsOrIff(Symbol(cons.node + "Left"), Or(Not(cons.guard), cons.value)))
                fList.append(EqualsOrIff(Symbol(cons.node + "Right"), Or(Not(cons.guard), Not(cons.value))))
        if is_unsat(And(fList)):
            return False
        return True

def GSTEMC(filename, assertions: TrajAssertions):
    # parse aig
    outs, louts, inputs = parseAiger(filename)
    # ckt_stt
    ckt_stt = {}
    # 从0开始的assertion加入队列 (0,1)
    visited = []
    queue = Queue()
    for item in assertions.getFromT(0):
        queue.put(item)

    while not queue.empty():
        (fromTime, toTime) = queue.get()
        antList = assertions.getAntListFromTo(fromTime, toTime)
        consList = assertions.getConsListFromTo(fromTime, toTime)


        if fromTime == 0:
            ckt_stt[(fromTime, toTime)] = { **stt_pred(antList,inputs), **latchInit(louts)}
        else:
            ckt_stt[(fromTime, toTime)] = { **post(antList, ckt_stt, outs, louts, inputs), **stt_pred(antList,inputs)}

        if not check(ckt_stt[(fromTime, toTime)],consList):
            return False

        for item in assertions.getFromT(toTime):
            if item not in visited:
                queue.put(item)
                visited.append(item)
    x = simplify(ckt_stt[(1,2)]['q'].left.substitute({Symbol('za'):FALSE()}))
    return True

def testGSTEMC():
    filename = './example/memory1x1.aag'
    # x= Symbol('x')
    # subs = {x:And(Symbol('y'),Symbol('z'))}
    # t = x.substitute(subs)
    assertions = TrajAssertions()
    # q0-1
    assertions.addAnt(isVar('we', TRUE(), 0, 1))
    assertions.addAnt(isVar('data', Symbol('zd'), 0, 1))
    assertions.addAnt(isVar('addr', Symbol('za'), 0, 1))
    # q1-1
    assertions.addAnt(isVar('we', Symbol('p'), 1, 1))
    assertions.addAnt(guard(Symbol('p'), 'addr', Not(Symbol('za')), 1, 1))
    # q1-2
    assertions.addAnt(isVar('we', FALSE(), 1, 2))
    assertions.addAnt(isVar('addr', Symbol('za'), 1, 2))
    assertions.addCons(isVar('q', Symbol('zd'), 1, 2))

    print(GSTEMC(filename, assertions))

testGSTEMC()
