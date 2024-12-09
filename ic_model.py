import random
import networkx as nx


def independent_cascade(graph, seed_node, max_steps=float('inf')):
    """
    Simulate the Independent Cascade (IC) model.

    Args:
        graph (nx.DiGraph): A directed graph representing the social network.
        seed_node (int): The initial node to start the diffusion.
        max_steps (int): Maximum number of diffusion steps.

    Returns:
        list: List of active nodes at the end of the diffusion process.
    """
    if not isinstance(graph, nx.DiGraph):
        raise TypeError("The graph must be a directed graph (nx.DiGraph).")

    active_nodes = {seed_node}
    newly_active = {seed_node}
    steps = 0

    while newly_active and steps < max_steps:
        next_active = set()
        for node in newly_active:
            for neighbor in graph.successors(node):
                if neighbor not in active_nodes:
                    activation_prob = graph[node][neighbor].get('weight', 0)
                    if random.random() < activation_prob:
                        next_active.add(neighbor)
        active_nodes.update(next_active)
        newly_active = next_active
        steps += 1

    return list(active_nodes)


def filter_active_subgraph(graph, active_nodes):
    """
    Create a subgraph containing only active nodes.

    Args:
        graph (nx.DiGraph): The original graph.
        active_nodes (list): List of active nodes.

    Returns:
        nx.DiGraph: A subgraph containing only active nodes.
    """
    return graph.subgraph(active_nodes).copy()


def find_reducible_subgraph(graph):
    """
    Identify the largest strongly connected component among active nodes.

    Args:
        graph (nx.DiGraph): A subgraph of active nodes.

    Returns:
        list: Nodes in the largest strongly connected component.
    """
    sccs = list(nx.strongly_connected_components(graph))
    largest_scc = max(sccs, key=len)
    return list(largest_scc)
