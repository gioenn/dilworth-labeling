import networkx as nx
from functools import reduce
import sys
import scipy as sp
import numpy as np

def label(G):
    label_vertex = {}
    stack = [x for x in G.nodes() if not G.predecessors(x)]
    id = 0

    def available_labels(node):
        res = []
        label = G.node[node]["label"]
        if label in label_vertex and label_vertex[label] == node:
            res.append(label)
        for pred in G.predecessors(node):
            res.extend(available_labels(pred))
        return res

    def pop():
        min = sys.maxint
        for node in stack:
            preds = G.predecessors(node)
            deg = G.in_degree(node)
            if (not preds or not len([x for x in preds if "label" not in G.node[x]])) and deg < min:
                res = node
                min = deg

        stack.remove(res)
        return res

    while len(stack) > 0:
        node = pop()
        node_data = G.node[node]
        preds = G.predecessors(node)

        # consider only the nodes with labels to be propageted
        candidates = [(G.node[x], y) for x in preds if G.node[x]["out_count"] > 0 for y in [available_labels(x)] if len(y) > 0]

        # if none create assign a new label
        if len(candidates) == 0:
            node_data["label"] = id
            id += 1
        else:
            # get the predecessor with the lowest out-degree
            best = reduce(lambda x, y:  x if x[0]["out_count"] < y[0]["out_count"] else y, candidates)
            node_data["label"] = best[1].pop() # assign an existing label

        for pred in preds:
            G.node[pred]["out_count"] -= 1

        for succ in G.successors(node):
            if "label" not in G.node[succ] and succ not in stack:
                stack.insert(0, succ)

        node_data["out_count"] = G.out_degree(node) # assign to the node its out-degree
        label_vertex[node_data["label"]] = node

    return id
    
def get_parallelism(G):
    return max(map(lambda x: len(x), list(nx.antichains(G))))
