from random import choice, randint

def exists(edges, n1, n2):
    for i in edges:
        if (i[0] == n1 and i[1] == n2) or (i[1] == n1 and i[0] == n2):
            return True
    return False

def MakeData():
    nodes = []
    edges = []

    for i in range(10):
        nodes.append(chr(ord('A') + i))

    for i in range(30):
        n1 = choice(nodes)
        n2 = choice(nodes)
        if not exists(edges, n1, n2):
            edges.append([
                n1,
                n2,
                randint(0, 100),
                randint(0, 100)
            ])

    return {
        "edges": edges,
        "nodes": nodes
    }