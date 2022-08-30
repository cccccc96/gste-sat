from aigParser import *
from checkEdge import *


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

def runCheckEdge():
    filename = './example/rbFIFO-3-15-3.aag'
    transitionSystem = parseAiger(filename)
    trajAssertion = FIFO_TrajAssertion(15)
    check = CheckEdge(transitionSystem, trajAssertion)
    check.run()

runCheckEdge()


