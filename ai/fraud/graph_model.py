import networkx as nx

G = nx.Graph()


def add_tx(user, device):
    G.add_edge(user, device)


def anomaly_score(user):
    return G.degree(user)
