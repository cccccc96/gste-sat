class TrajForm:
    pass

class isVar(TrajForm):
    """
        四元组(node,value, fromTime , toTime)
    """

    def __init__(self, node, value, fromTime, toTime):
        self.node = node
        self.value = value
        self.fromTime = fromTime
        self.toTime = toTime

class guard(TrajForm):
    """
        五元组(guard,node,value, fromTime , toTime)
    """

    def __init__(self,guard, node, value, fromTime, toTime):
        self.guard = guard
        self.node = node
        self.value = value
        self.fromTime = fromTime
        self.toTime = toTime

class TrajAssertions:
    def __init__(self):
        self.antList = []
        self.consList = []

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
            if ant.fromTime == T:
                if (ant.fromTime,ant.toTime) not in res:
                    res.append((ant.fromTime,ant.toTime))
        return res

    def getAntListFromTo(self, fromTime, toTime):
        # 根据fromTime 和 toTime 获取对应的AntList列表
        res = []
        for ant in self.antList:
            if ant.fromTime == fromTime and ant.toTime == toTime:
                res.append(ant)
        return res

    def getConsListFromTo(self, fromTime, toTime):
        # 根据fromTime 和 toTime 获取对应的ConsList列表
        res = []
        for cons in self.consList:
            if cons.fromTime == fromTime and cons.toTime == toTime:
                res.append(cons)
        return res