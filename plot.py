import graphviz

def render(G):
    dot = graphviz.Digraph(comment='My plot')

    for n in sorted(G.nodes()):
        if "label" in G.node[n]:
            dot.node(str(n), "S{}\n<{}>".format(n, G.node[n]["label"]))
        else:
            dot.node(str(n), "S{}".format(n))

        for p in G.predecessors(n):
            dot.edge(str(p), str(n))

    dot.render(view=True)
