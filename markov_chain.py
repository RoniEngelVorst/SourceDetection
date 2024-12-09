import networkx as nx
import numpy as np


def convert_to_markov_chain(graph, method="self-loops"):
    """
    Convert a social network graph into a Markov chain.

    Args:
        graph (nx.DiGraph): Input directed graph.
        method (str): Conversion method, either "self-loops" or "no-loops".

    Returns:
        nx.DiGraph: Markov chain graph.
    """
    markov_chain = graph.reverse(copy=True)
    max_in_degree = max(dict(markov_chain.in_degree(weight="weight")).values())

    for u, v in markov_chain.edges:
        markov_chain[u][v]['weight'] /= graph.in_degree(v, weight="weight")

    if method == "self-loops":
        for node in markov_chain.nodes:
            self_loop_weight = max_in_degree - graph.in_degree(node, weight="weight")
            markov_chain.add_edge(node, node, weight=self_loop_weight)

    normalize_edge_weights(markov_chain)
    return markov_chain


def normalize_edge_weights(graph):
    """
    Normalize edge weights so that outgoing edges from a node sum to 1.

    Args:
        graph (nx.DiGraph): A directed graph.
    """
    for node in graph.nodes:
        total_weight = sum(data['weight'] for _, _, data in graph.out_edges(node, data=True))
        if total_weight > 0:
            for _, v, data in graph.out_edges(node, data=True):
                data['weight'] /= total_weight


def compute_stationary_distribution(graph):
    """
    Compute the stationary distribution of a Markov chain.

    Args:
        graph (nx.DiGraph): Markov chain graph.

    Returns:
        dict: Stationary distribution {node: probability}.
    """
    adjacency_matrix = nx.to_numpy_array(graph, weight='weight')
    eigenvalues, eigenvectors = np.linalg.eig(adjacency_matrix.T)
    stationary_vector = eigenvectors[:, np.isclose(eigenvalues, 1)].flatten().real
    stationary_distribution = stationary_vector / stationary_vector.sum()
    return dict(zip(graph.nodes, stationary_distribution))
