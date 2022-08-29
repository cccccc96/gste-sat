from util import *

"""
trajF is restricted to these types
    - isT
    - isF
    - eq a b 
        - a is boolean and b is boolean -> a==b
        - a is BITVEC(i) and b is BITVEC(i) -> a_0==b_0 /\ .../\a_i==b_i
    - trajF /\ trajF
    
undinfined funciton
    - plusN(head,i)
        - an implementation of full adder without top carry
        - return a list of sum
"""


def isT(boolNode_name):
    assert isinstance(SORT.sort_map[boolNode_name], BOOLEAN)
    boolNode = Bool(boolNode_name)
    return boolNode == True


def isF(boolNode_name):
    assert isinstance(SORT.sort_map[boolNode_name], BOOLEAN)
    boolNode = Bool(boolNode_name)
    return boolNode == False


class PLUSN:
    """
        implementation of a full adder without top carry
        plusN(bvNode_name,n)
        e.g. plusN(head,3)
    :param bvNode_name:
    :param n:
    :return: sum list -> [sum[0],sum[1],...,sum[j]] (bvNode is BITVEC(j+1))
    """

    def __init__(self, bvNode_name: str, n: int):
        self.bvNode_name = bvNode_name
        self.n = n

    def Xor(self, a, b):
        """
            boolean xor boolean
        :param a: z3_boolean_var
        :param b: z3_boolean_var
        :return:
        """
        return simplify(
            Or(
                And(Not(a), b),
                And(a, Not(b))
            )
        )

    def s(self, a, b, cin):
        return simplify(
            Xor(cin, Xor(a, b))
        )

    def c(self, a, b, cin):
        return simplify(
            Or(
                And(a, b),
                And(
                    Xor(a, b),
                    cin
                )
            )
        )

    def intToBooleanList(self, n: int, length: int):
        t = bin(n)[2:]
        res = []
        for i in range(length):
            if i < len(t):
                res.append((True if t[-i - 1] == '1' else False))
            else:
                res.append(False)
        return res

    def sumList(self):
        bvNode_name = self.bvNode_name
        n = self.n
        assert isinstance(SORT.sort_map[bvNode_name], BITVEC)
        length = SORT.sort_map[bvNode_name].length
        l = []
        for i in range(length):
            l.append(Bool('%s[%d]' % (bvNode_name, i)))
        r = self.intToBooleanList(n, length)
        carry = []
        carry.append(False)
        for i in range(1, length):
            carry.append(self.c(l[i - 1], r[i - 1], carry[i - 1]))
        sum = []
        for i in range(length):
            sum.append(self.s(l[i], r[i], carry[i]))
        return sum


class READ:

    def __init__(self, arr_name:str, idx):
        '''

        :param arr_name: str
        :param idx: str/
        '''
        self.arr_name = arr_name
        self.idx = idx
        self.idx_len = SORT.sort_map[arr_name].idx_len
        self.ele_len = SORT.sort_map[arr_name].ele_len

    def idxNameToInt(self,idxName:str):
        res = 0
        length = SORT.sort_map[idxName].length
        for i in range(length):
            boolean_var = Bool("%s[%d]" % (idxName,i))
            res += If(
                boolean_var,
                2**i,
                0
            )
        return simplify(res)

    def eleList(self):
        idx_val = self.idxNameToInt(self.idx)
        res = []
        for ele_id in range(self.ele_len):
            ele = If(
                idx_val==1,
                Bool('%s[%d][%d]' % (self.idx, 1,ele_id)),
                Bool('%s[%d][%d]' % (self.idx, 0,ele_id))
            )
            for i in range(2,self.idx_len):
                ele = If(
                    idx_val == i,
                    Bool('%s[%d][%d]' % (self.idx, i,ele_id)),
                    ele
                )
            res.append(simplify(ele))
        return res

def EQUAL(a,b):
    if isinstance(a,str) and isinstance(b,str):
        length = SORT.sort_map[a]
        res = []
        for i in range(length):
            res.append(
                Bool("%s[%d]" % (a,i)) == Bool("%s[%d]" % (b,i))
            )
        return And(res)
    elif isinstance(b,PLUSN):
        length = SORT.sort_map[a]
        b_list = b.sumList()
        res = []
        for i in range(length):
            res.append(
                Bool("%s[%d]" % (a,i)) == b_list[i]
            )
        return And(res)



class TrajFormula:
    def __init__(self, formula, sourceTime, sinkTime):
        self.formula = formula
        self.sourceTime = sourceTime
        self.sinkTime = sinkTime

    def __str__(self):
        return "%s  %d  %d " % (str(self.formula), self.sourceTime, self.sinkTime)


class MuFormula:
    def __init__(self, formula, time):
        self.formula = formula
        self.time = time


class TrajAssertions:
    def __init__(self):
        self.antList = []
        self.consList = []

    def getVertexs(self):
        res = set()
        for ant in self.antList:
            res.add(ant.sourceTime)
            res.add(ant.sinkTime)
        return res

    def addAnt(self, ant):
        # antecedent
        self.antList.append(ant)

    def addCons(self, cons):
        # consequence
        self.consList.append(cons)

    def getFromT(self, T):
        # 取出从T时刻开始的(T,T) / (T,T+1)
        # return: (T,T2)
        res = []
        for ant in self.antList:
            if ant.sourceTime == T:
                if (ant.sourceTime, ant.sinkTime) not in res:
                    res.append((ant.sourceTime, ant.sinkTime))
        return res

    def getAntFromTo(self, sourceTime, sinkTime):
        res = []
        for ant in self.antList:
            if ant.sourceTime == sourceTime and ant.sinkTime == sinkTime:
                res.append(ant.formula)
        if len(res) == 1:
            return res[0]
        return And(res)

    def getAntListFromTo(self, sourceTime, sinkTime):
        # 根据sourceTime 和 sinkTime 获取对应的AntList列表
        res = []
        for ant in self.antList:
            if ant.sourceTime == sourceTime and ant.sinkTime == sinkTime:
                res.append(ant.formula)
        return res

    def getConsFromTo(self, sourceTime, sinkTime):
        # 根据sourceTime 和 sinkTime 获取对应的ConsList列表
        res = []
        for cons in self.consList:
            if cons.sourceTime == sourceTime and cons.sinkTime == sinkTime:
                res.append(cons.formula)
        if len(res) == 0:
            return True
        return And(res)
