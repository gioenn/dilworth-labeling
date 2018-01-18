import networkx as nx

class LabeledDiGraph(nx.DiGraph):

    def label(self):
        chains, antichain = self.__bogart()
        id = 0
        for chain in chains:
            for n in chain:
                self.node[n]['label'] = id
            id+=1

        return chains, antichain, id

    def get_parallelism(self):
        return max(map(lambda x: len(x), list(nx.antichains(self))))

    def __bogart(self):

        self.I = {}
        self.C = []

        for n in self.nodes():
            self.I[n] = nx.ancestors(self, n)
            self.C.append([n])

        oldchains = list(self.C)

        self.__reduce()

        while self.C != oldchains:
            oldchains = list(self.C)
            self.__reduce()

        return list(self.C), list(self.E)

    def __reduce(self):

        N = []
        M = []

        self.E = []
        self.USED = {}
        self.PAIR = {}

        for n in self.nodes():
            self.USED[n] = False
            self.PAIR[n] = None

        for c in self.C:
            N.append(c[0])
            self.E.append(c[0])

        while len(N) > 0:
            for a in N:
                J = self.I[a]
                for b in J:
                    if not self.USED[b]:
                        T = self.__TAIL(b)
                        if len(T) > 1:
                            aa = T[1]
                            self.PAIR[aa] = (a, b)
                            self.USED[b] = True
                            self.E.append(aa)
                            M.append(aa)
                        else:
                            return self.__redochains(a, b)
            N = list(M)
            M = []

    def __redochains(self, a, b):

        self.__modtail(b, self.__TAIL(a))

        if self.PAIR[a]:
            self.__redochains(self.PAIR[a][0], self.PAIR[a][1])
        else:
            self.C.remove(self.__TAIL(a))

    def __TAIL(self, x):
        for c in self.C:
            if x in c:
                index = c.index(x)
                return c[index:]

    def __modtail(self, x, tail):
        for c in self.C:
            if x in c:
                index = c.index(x)+1
                del c[index:]
                c.extend(tail)

    def __printtails(self):
        for n in self.nodes():
            print(str(n)+":"+" "+str(self.__TAIL(self.C,n)))


def random(n, p):
    RNDG = nx.fast_gnp_random_graph(n, p, directed=True)
    return LabeledDiGraph([(u,v) for (u,v) in RNDG.edges() if u<v])
