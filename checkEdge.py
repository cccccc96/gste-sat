from util import *
from trajFormula import *

class CheckEdge:
    def __init__(self, transitionSystem: TransitionSystem, trajAssertion: TrajAssertions):
        self.transitionSystem = transitionSystem
        self.trajAssertion = trajAssertion

    def get_subs(self, i):
        # get vars@i and vars@i+1, stored in tuples
        subs_i = []
        for v in self.transitionSystem.variables:
            subs_i.append((v, at_time(v, i)))
            subs_i.append((next_var(v), at_time(v, i + 1)))
        return subs_i


    def getAnt_Edge(self, edge):
        """
            get ant in specific edge and substitute vars with vars@time
        :param edge: (source, sink)
        :param time: time
        :return: ant_edge@time
        """
        (source,sink) = edge
        ant_edge = self.trajAssertion.getAntFromTo(source, sink)
        return ant_edge

    def getMu_edge(self, edge):
        (source, sink) = edge
        mu = self.trajAssertion.getMu(source)
        return mu

    # def getCons(self, edge):
    #     (source, sink) = edge
    #     consList = []
    #     edgeList_from_sink = self.trajAssertion.getFromT(sink)
    #     for (source_,sink_) in edgeList_from_sink:
    #         consList.append( self.trajAssertion.getConsFromTo(source_, sink_))
    #     cons = simplify(And(consList))
    #     subs = []
    #     for var in self.transitionSystem.variables:
    #         subs.append((var, next_var(var)))
    #     if cons is not True:
    #         cons = substitute(cons,subs)
    #     return cons

    def getCons(self, edge):
        (source, sink) = edge
        mu = self.trajAssertion.getMu(sink)
        subs = []
        for var in self.transitionSystem.variables:
            subs.append((var, next_var(var)))
        if mu is not True:
            mu = substitute(mu,subs)
        return mu

    def match(self, cur_state, cons, edge):
        f = Not(
            Implies(cur_state, cons)
        )
        if is_sat(f):
            print('not match',edge)
            return False
        print('match',edge)
        return True

    def run(self):
        visited = []
        edge_queue = []
        edgeList_from_0 = self.trajAssertion.getFromT(0)
        for edge in edgeList_from_0:
            edge_queue.insert(0, edge)
        while len(edge_queue) != 0:
            edge = edge_queue.pop()
            visited.append(edge)
            (source,sink) = edge
            regs_pre = self.transitionSystem.regs
            ant_pre = self.getAnt_Edge(edge)
            T = self.transitionSystem.trans
            mu = self.getMu_edge(edge)
            cur_state = Exists(
                regs_pre,
                And(
                    ant_pre,
                    mu,
                    T
                )
            )
            simpl = Tactic("simplify")
            # eliminator = Tactic("qe2")
            # t = Then(simpl, eliminator, simpl)
            t = Then(simpl,simpl)

            cur_state = t(cur_state).as_expr()
            # if edge == (6,4):
            #     print(edge)
            #     print('mu',mu)
            #     print('ant_pre',ant_pre)
            #     print('cur_state',cur_state)

            cons = self.getCons(edge)
            self.match(cur_state,cons,edge)

            edgeList_from_source = self.trajAssertion.getFromT(sink)
            for edge in edgeList_from_source:
                if edge not in visited:
                    edge_queue.insert(0, edge)
