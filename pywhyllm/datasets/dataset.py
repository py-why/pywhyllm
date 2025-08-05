from typing import List, Protocol

class Dataset(Protocol):
    
    def graph(self):
        """
        Output the ground truth graph associated with the dataset. 

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

