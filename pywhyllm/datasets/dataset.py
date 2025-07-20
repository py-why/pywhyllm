from typing import List, Protocol

class Dataset(Protocol):
    
    def graph(self):
        """
        Output the graph associated with the dataset. 

        Args:
        Returns:
            A networkx graph 
        """
        pass

    def data(self):
        """
        Output the data associated with the dataset.

        Returns:
            A numpy array containing the data
        """
        pass

    def generate_data(self):
        """
        Generate synthetic data based on the dataset's causal graph.

        Returns:
            A numpy array containing the synthetic data
        """
        pass
