import numpy as np
from markov_chain import convert_to_markov_chain, compute_stationary_distribution


def calculate_source_probabilities(graph, active_subgraph, method="self-loops"):
    """
    Calculate source probabilities for active nodes using Markov chain methods.

    Args:
        graph (nx.DiGraph): Original graph.
        active_subgraph (nx.DiGraph): Subgraph of active nodes.
        method (str): Conversion method, "self-loops" or "no-loops".

    Returns:
        dict: Source probabilities {node: probability}.
    """
    markov_chain = convert_to_markov_chain(active_subgraph, method)
    stationary_distribution = compute_stationary_distribution(markov_chain)

    if method == "no-loops":
        weighted_in_degrees = {node: graph.in_degree(node, weight="weight") for node in active_subgraph.nodes}
        stationary_distribution = {
            node: stationary_distribution[node] / weighted_in_degrees[node]
            for node in stationary_distribution
        }
        normalize_probabilities(stationary_distribution)

    return stationary_distribution


def normalize_probabilities(probabilities):
    """
    Normalize probabilities so they sum to 1.

    Args:
        probabilities (dict): Dictionary of probabilities.
    """
    total = sum(probabilities.values())
    for key in probabilities:
        probabilities[key] /= total


def identify_source(probabilities):
    """
    Identify the most likely source node.

    Args:
        probabilities (dict): Source probabilities.

    Returns:
        int: Node with the highest probability of being the source.
    """
    return max(probabilities, key=probabilities.get)
