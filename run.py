from aigParser import *
from util import *
from trajFormula import *
from checkEdge import *


def test_traj2(LAST):
    trajAssertion = TrajAssertions()
    ant = And(isF('rst'), isT('push'), EQUAL('dataIn', 'D'))
    cons = And(isF('empty'), isF('full'))
    trajAssertion.addAnt(TrajFormula(ant, 7, 10))

    mu = And(EQUAL('tail', PLUSN('head', LAST)), isF('empty'), isF('full'))
    trajAssertion.addMu(MuFormula(mu,7))

    mu = And(EQUAL('tail', 'head'), isF('empty'), isF('full'),
             EQUAL(READ('mem', PLUSN('head', i)), 'D'))





def test_traj(LAST):
    trajAssertion = TrajAssertions()
    trajAssertion.addAnt(TrajFormula(isT('rst'), 0, 1))
    ant = And(isF('rst'), isT('push'))
    cons = And(isT('empty'), isF('full'))
    trajAssertion.addAnt(TrajFormula(ant, 1,  3))
    trajAssertion.addCons(TrajFormula(cons, 1,  3))

    ant = And(isF('rst'), isT('push'), EQUAL('dataIn', 'D'))
    cons = And(isF('empty'), isF('full'))
    trajAssertion.addAnt(TrajFormula(ant, 3, 6))
    trajAssertion.addCons(TrajFormula(cons, 3, 6))

    ant = And(isF('rst'), isF('push'), isT('pop'))
    trajAssertion.addAnt(TrajFormula(ant, 6, 4))

    ant = And(isF('rst'), isF('push'), isT('pop'))
    cons = And(EQUAL('dataOut', 'D'))
    trajAssertion.addAnt(TrajFormula(ant, 4, 1))
    trajAssertion.addCons(TrajFormula(cons, 4, 1))


    mu = And(EQUAL('tail', 'head'), isT('empty'), isF('full'))
    trajAssertion.addMu(MuFormula(mu, 1))

    mu = And(EQUAL('tail', PLUSN('head', 1)), isF('empty'), isF('full'))
    trajAssertion.addMu(MuFormula(mu, 3))

    mu = And(EQUAL('tail', PLUSN('head', 1)), isF('empty'), isF('full'), EQUAL(READ('mem', 'head'), 'D'))
    trajAssertion.addMu(MuFormula(mu, 4))

    mu = And(EQUAL('tail', PLUSN('head', 2)), isF('empty'), isF('full'),
             EQUAL(READ('mem', PLUSN('head', 1)), 'D'))
    # print(READ('mem', 'head').eleList())
    # print('--'*20)
    # print(PLUSN('head', 1).sumList())
    # print('--' * 20)
    # print(READ('mem', PLUSN('head', 1)).eleList())
    trajAssertion.addMu(MuFormula(mu, 6))

    return trajAssertion








def FIFO_TrajAssertion(LAST):
    trajAssertion = TrajAssertions()

    '''
        ant/cons
    '''

    # reset 0-1
    trajAssertion.addAnt(TrajFormula(isT('rst'), 0, 1))

    # push without D
    # 1->...->2*i+1->2*i+3->...->2*LAST+3
    for i in range(LAST + 1):
        ant = And(isF('rst'), isT('push'))
        if i == 0:
            cons = And(isT('empty'), isF('full'))
        else:
            cons = And(isF('empty'), isF('full'))
        trajAssertion.addAnt(TrajFormula(ant, 2 * i + 1, 2 * i + 3))
        trajAssertion.addCons(TrajFormula(cons, 2 * i + 1, 2 * i + 3))

    # pop without D
    # 2*LAST+3->...->2*i+3->2*i+1->...->1
    for i in range(1, LAST + 1):
        ant = And(isF('rst'), isF('push'), isT('pop'))
        if i == LAST:
            cons = And(isF('empty'), isT('full'))
        else:
            cons = And(isF('empty'), isF('full'))
        trajAssertion.addAnt(TrajFormula(ant, 2 * i + 3, 2 * i + 1))
        trajAssertion.addCons(TrajFormula(cons, 2 * i + 3, 2 * i + 1))

    # push D
    for i in range(LAST + 1):
        ant = And(isF('rst'), isT('push'), EQUAL('dataIn', 'D'))
        if i == 0:
            cons = And(isT('empty'), isF('full'))
        else:
            cons = And(isF('empty'), isF('full'))
        trajAssertion.addAnt(TrajFormula(ant, 2 * i + 1, 2 * i + 4))
        trajAssertion.addCons(TrajFormula(cons, 2 * i + 1, 2 * i + 4))

    for i in range(LAST):
        ant = And(isF('rst'), isF('push'), isT('pop'))
        trajAssertion.addAnt(TrajFormula(ant, 2 * i + 6, 2 * i + 4))

    # 4->1
    ant = And(isF('rst'), isF('push'), isT('pop'))
    cons = And(EQUAL('dataOut', 'D'))
    trajAssertion.addAnt(TrajFormula(ant, 4, 1))
    trajAssertion.addCons(TrajFormula(cons, 4, 1))

    '''
        mu
    '''

    # 2*i+1
    #   - tail=plusN(head,i) & !empty & !full
    # 1
    #   - tail=head & empty & !full
    # 2*LAST+3
    #   - tail=head & !empty & full
    for i in range(LAST + 2):
        if i == 0:
            mu = And(EQUAL('tail', 'head'), isT('empty'), isF('full'))
        elif i == LAST + 1:
            mu = And(EQUAL('tail', 'head'), isF('empty'), isT('full'))
        else:
            mu = And(EQUAL('tail', PLUSN('head', i)), isF('empty'), isF('full'))
        trajAssertion.addMu(MuFormula(mu, 2 * i + 1))

    for i in range(LAST + 1):
        if i == 0:
            mu = And(EQUAL('tail', PLUSN('head', 1)), isF('empty'), isF('full'), EQUAL(READ('mem', 'head'), 'D'))
        elif i == LAST:
            mu = And(EQUAL('tail', 'head'), isF('empty'), isT('full'),
                     EQUAL(READ('mem', PLUSN('head', i)), 'D'))
        else:
            mu = And(EQUAL('tail', PLUSN('head', i + 1)), isF('empty'), isF('full'),
                     EQUAL(READ('mem', PLUSN('head', i)), 'D'))
        trajAssertion.addMu(MuFormula(mu, 2 * i + 4))

    return trajAssertion


filename = './example/rbFIFO-1-3-1_NoOutput.aag'
transitionSystem = parseAiger(filename)
trajAssertion = FIFO_TrajAssertion(3)
check = CheckEdge(transitionSystem, trajAssertion)
check.run()

# y = READ('mem','head')
# # y2 = y.idxNameToInt('head')
# y3 = y.eleList()
# for item in y3:
#     print(item)
# solve(y2==2)
# print(y2)

print(1)
