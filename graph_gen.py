import networkx as nx
import random


def generate_random_graph(num_nodes, edge_probability):
    """
    Generate a random directed graph using the Erdős–Rényi model.

    Args:
        num_nodes (int): Number of nodes in the graph.
        edge_probability (float): Probability of an edge between two nodes.

    Returns:
        nx.DiGraph: A generated random directed graph.
    """
    return nx.erdos_renyi_graph(num_nodes, edge_probability, directed=True)


def generate_grid_graph(rows, cols):
    """
    Generate a 2D grid graph.

    Args:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.

    Returns:
        nx.Graph: A generated grid graph.
    """
    return nx.grid_2d_graph(rows, cols)


def add_random_weights(graph, weight_range=(1, 10)):
    """
    Add random weights to all edges in a graph.

    Args:
        graph (nx.Graph): The graph to which weights are added.
        weight_range (tuple): Range (min, max) for the random weights.

    Returns:
        nx.Graph: The graph with weighted edges.
    """
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.randint(*weight_range)
    return graph


def convert_to_undirected(graph):
    """
    Convert a directed graph to an undirected one.

    Args:
        graph (nx.DiGraph or nx.Graph): Input graph.

    Returns:
        nx.Graph: An undirected version of the graph.
    """
    if isinstance(graph, nx.DiGraph):
        return graph.to_undirected()
    return graph


def visualize_graph(graph, with_weights=False):
    """
    Visualize a graph using NetworkX and Matplotlib.

    Args:
        graph (nx.Graph): The graph to visualize.
        with_weights (bool): Whether to display edge weights.

    Returns:
        None: Displays the graph plot.
    """
    import matplotlib.pyplot as plt

    pos = nx.spring_layout(graph)  # Spring layout for visualization
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10)

    if with_weights:
        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.show()

def generate_graphs_from_original():
    """
    Generate graphs G1 to G14 as defined in the original project.

    Returns:
        dict: A dictionary of graph names mapped to their generated graphs.
    """
    graph_params = {
        "G1": {"num_nodes": 500, "edge_prob": 0.1},
        "G2": {"num_nodes": 1000, "edge_prob": 0.1},
        "G3": {"num_nodes": 2000, "edge_prob": 0.1},
        "G4": {"num_nodes": 3000, "edge_prob": 0.1},
        "G5": {"num_nodes": 4000, "edge_prob": 0.1},
        "G6": {"num_nodes": 5000, "edge_prob": 0.1},
        "G7": {"num_nodes": 500, "edge_prob": 0.0416},
        "G8": {"num_nodes": 1000, "edge_prob": 0.02},
        "G9": {"num_nodes": 2000, "edge_prob": 0.0101},
        "G10": {"num_nodes": 3000, "edge_prob": 0.0067},
        "G11": {"num_nodes": 4000, "edge_prob": 0.0052},
        "G12": {"num_nodes": 5000, "edge_prob": 0.0041},
        "G13": {"num_nodes": 10000, "edge_prob": 0.002},
        "G14": {"num_nodes": 15000, "edge_prob": 0.0013},
    }

    graphs = {}
    for name, params in graph_params.items():
        graphs[name] = generate_random_graph(params["num_nodes"], params["edge_prob"])
    return graphs
