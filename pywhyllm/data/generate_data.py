

def generate_data(graph, *args, **kwargs):
    """
    Generate synthetic data based on a causal graph.
    Arguments may be added as the functionality is developed.
    Args:
        graph: A Networkx graph
    Returns:
        A numpy array containing the synthetic data
    """
    pass


import numpy as np
import networkx as nx
from typing import Union, Optional


def generate_data(graph: nx.DiGraph, n_samples: int = 1000,
                  noise_std: float = 0.1, seed: Optional[int] = None) -> np.ndarray:
    """
    Generate synthetic data based on a causal graph.

    Args:
        graph: A NetworkX DiGraph representing the causal structure.
        n_samples: Number of data samples to generate (default: 1000).
        noise_std: Standard deviation of Gaussian noise added to each variable (default: 0.1).
        seed: Random seed for reproducibility (default: None).

    Returns:
        A NumPy array of shape (n_samples, n_nodes) containing the synthetic data.
    """
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Input graph must be a directed acyclic graph (DAG).")

    # Set random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Get topological order to process nodes (ensures parents are processed before children)
    nodes = list(nx.topological_sort(graph))
    n_nodes = len(nodes)

    # Initialize data array: rows = samples, columns = nodes
    data = np.zeros((n_samples, n_nodes))

    # Map nodes to column indices for easy access
    node_to_index = {node: idx for idx, node in enumerate(nodes)}

    for node in nodes:
        node_idx = node_to_index[node]
        parents = list(graph.predecessors(node))

        if not parents:
            # If node has no parents, generate from a standard normal distribution
            data[:, node_idx] = np.random.normal(0, 1, n_samples)
        else:
            # Generate data as a linear combination of parent values plus noise
            # You can modify this to include nonlinear relationships
            parent_indices = [node_to_index[parent] for parent in parents]
            parent_data = data[:, parent_indices]  # Shape: (n_samples, n_parents)

            # Random weights for linear combination (can be customized)
            weights = np.random.uniform(-1, 1, len(parents))

            # Compute node values as weighted sum of parents
            node_values = parent_data @ weights

            # Add Gaussian noise
            noise = np.random.normal(0, noise_std, n_samples)
            data[:, node_idx] = node_values + noise

    return data
