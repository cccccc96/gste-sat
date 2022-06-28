from pysmt.shortcuts import *


class DualSymbol:
    """
        双轨编码:
            DualSymbol:(nameLeft,nameRight)
            x = (T,T)
            T = (T,F)
            F = (F,T)
            Z = (F,F)
        运算符重载:
            (a1,a2)&(b1,b2) = (a1&b1,a2|b2)
            ~(a1,a2) = (a2,a1)
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __and__(self, other):
        # &重载
        return DualSymbol(And(self.left, other.left), Or(self.right, other.right))

    def __invert__(self):
        # ~重载
        return DualSymbol(self.right, self.left)

    def __str__(self):
        return "(" + serialize(simplify(self.left)) + "," + serialize(simplify(self.right)) + ")"

    def substitute(self, subs):
        """

        :param subs: {name:dualSymbol(f1,f2)}
        :return:
        """

        # 修改subs成 {Symbol(nameLeft):f1,Symbol(nameRight):f2}
        newSubs = {}
        for name, dualSymbol in subs.items():
            newSubs[Symbol(name + "Left")] = dualSymbol.left
            newSubs[Symbol(name + "Right")] = dualSymbol.right

        return DualSymbol(simplify(self.left.substitute(newSubs)), simplify(self.right.substitute(newSubs)))
