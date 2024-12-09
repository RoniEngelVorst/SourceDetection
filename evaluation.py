import random
import networkx as nx
from ic_model import independent_cascade, filter_active_subgraph, find_reducible_subgraph
from source_detection import calculate_source_probabilities, identify_source
from graph_gen import generate_random_graph
import matplotlib.pyplot as plt


def run_experiment(graph, seed_node, method="self-loops", min_active_nodes=20):
    """
    Run a single experiment for source detection.

    Args:
        graph (nx.DiGraph): The social network graph.
        seed_node (int): Initial source node for the diffusion.
        method (str): Source detection method ("self-loops" or "no-loops").
        min_active_nodes (int): Minimum active nodes for valid diffusion.

    Returns:
        dict: Experiment results including true source, predicted source, and probabilities.
    """
    # Simulate diffusion
    active_nodes = independent_cascade(graph, seed_node)
    if len(active_nodes) < min_active_nodes:
        return None

    # Filter active subgraph and identify reducible subgraph
    active_subgraph = filter_active_subgraph(graph, active_nodes)
    reducible_subgraph_nodes = find_reducible_subgraph(active_subgraph)
    reducible_subgraph = active_subgraph.subgraph(reducible_subgraph_nodes).copy()

    # Calculate source probabilities and identify source
    probabilities = calculate_source_probabilities(graph, reducible_subgraph, method)
    predicted_source = identify_source(probabilities)

    return {
        "true_source": seed_node,
        "predicted_source": predicted_source,
        "probabilities": probabilities,
    }


def evaluate_on_random_graphs(num_graphs=10, num_nodes=100, edge_prob=0.1, method="self-loops"):
    """
    Evaluate source detection methods on random graphs.

    Args:
        num_graphs (int): Number of random graphs to generate.
        num_nodes (int): Number of nodes in each graph.
        edge_prob (float): Probability of an edge existing between nodes.
        method (str): Source detection method ("self-loops" or "no-loops").

    Returns:
        list: Experiment results for each graph.
    """
    results = []
    for _ in range(num_graphs):
        graph = generate_random_graph(num_nodes, edge_prob)
        seed_node = random.choice(list(graph.nodes))
        result = run_experiment(graph, seed_node, method)
        if result:
            results.append(result)
    return results


def summarize_results(results):
    """
    Summarize experiment results.

    Args:
        results (list): List of experiment results.

    Returns:
        dict: Summary statistics including accuracy and average probabilities.
    """
    correct_predictions = sum(1 for r in results if r["true_source"] == r["predicted_source"])
    accuracy = correct_predictions / len(results) if results else 0
    return {"accuracy": accuracy, "total_experiments": len(results)}


def plot_probabilities(results):
    """
    Plot source probabilities for experiments.

    Args:
        results (list): List of experiment results.
    """
    for result in results:
        probabilities = result["probabilities"]
        plt.figure()
        plt.bar(probabilities.keys(), probabilities.values())
        plt.title(f"True Source: {result['true_source']}, Predicted: {result['predicted_source']}")
        plt.xlabel("Node")
        plt.ylabel("Probability")
        plt.show()
