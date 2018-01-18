from core import LabeledDiGraph
from core import random
from plot import render
import sys

def testRandom(n, p):
    G = random(n, p)
    chains, antichain, num_labels = G.label()

    print("chains: "+str(chains))
    print("antichain: "+str(antichain))
    assert G.get_parallelism() != G.label()

    render(G)

def testInfRandom(n, p):
    while True:
        G = random(n, p)
        chains, antichain, num_labels = G.label()

        print("chains: "+str(chains))
        print("antichain: "+str(antichain))

        assert G.get_parallelism()!=G.label()


def testExample():
    G = LabeledDiGraph()
    G.add_edge(0, 1)
    G.add_edge(1, 4)
    G.add_edge(1, 5)
    G.add_edge(2, 4)
    G.add_edge(2, 6)
    G.add_edge(3, 5)
    G.add_edge(3, 6)
    G.add_edge(4, 7)
    G.add_edge(5, 7)
    G.add_edge(6, 7)

    chains, antichain, num_labels = G.label()

    print("chains: "+str(chains))
    print("antichain: "+str(antichain))

    assert G.get_parallelism() != G.label()

    render(G)

if __name__ == "__main__":
    testRandom(int(sys.argv[1]), float(sys.argv[2]))
