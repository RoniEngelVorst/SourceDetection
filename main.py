from evaluation import run_experiment, summarize_results
from graph_gen import generate_graphs_from_original
import random

def main():
    """
    Main function to evaluate source detection on predefined graphs G1 to G14.
    """
    detection_method = "self-loops"  # or "no-loops"
    min_active_nodes = 10  # Lowering the threshold to 10
    edge_probability = 0.1  # Can try increasing this value to something like 0.2 or 0.3

    print("Generating graphs G1 to G14...")
    graphs = generate_graphs_from_original()

    results = []
    for name, graph in graphs.items():
        print(f"Running experiment on {name}...")
        seed_node = random.choice(list(graph.nodes))
        result = run_experiment(graph, seed_node, method=detection_method, min_active_nodes=min_active_nodes)
        if result:
            results.append(result)
        else:
            print(f"Graph {name} did not meet minimum active node requirements.")

    # Summarize and display results
    summary = summarize_results(results)
    print(f"Accuracy: {summary['accuracy']:.2f}")
    print(f"Total Experiments: {summary['total_experiments']}")

if __name__ == "__main__":
    main()
