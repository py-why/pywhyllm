import logging
import re
from typing import List

from .simple_model_suggester import SimpleModelSuggester


class AugmentedModelSuggesterScientific(SimpleModelSuggester):
    """
        A class that extends SimpleModelSuggester and currently provides methods for suggesting causal relationships between variables by leveraging user-given scientific documents.

        Methods:
        - suggest_variables(document (what type??)) -> List[str]
            Suggests a list of relevant variables given a scientific document from the user and returns a list of the variables.
        - suggest_pairwise_relationship(document, variable1: str, variable2: str) -> List[str]:
            Suggests the causal relationship between two variables and returns a list containing the cause, effect, and a description of the relationship.
        - suggest_relationships(document, variables: List[str]) -> dict: A dictionary of edges found between variables, where the keys are tuples representing the causal relationship between two variables,
            and the values are the strength of the relationship.
        """

    def __init__(self, llm):
        super().__init__(llm)

    def suggest_variables(self, document):
        """
            Suggests a cause-and-effect relationship between two variables.

            Args:
                document: scientific document provided by the user

            Returns:
                list: A list of suggested relevant variables based on the provided scientific document."""

    def suggest_pairwise_relationship(self, document, variable1: str, variable2: str):
        """
            Suggests a cause-and-effect relationship between two variables.

            Args:
                document: scientific document provided by the user
                variable1 (str): The name of the first variable.
                variable2 (str): The name of the second variable.

            Returns:
                list: A list containing the suggested cause variable, the suggested effect variable, and a description of the reasoning behind the suggestion.  If there is no relationship between the two variables, the first two elements will be None.
            """

    def suggest_relationships(self, document, variables: List[str]):
        """
        Given a list of variables, suggests relationships between them by querying for pairwise relationships.

        Args:
            document: scientific document provided by the user
            variables (List[str]): A list of variable names.

        Returns:
            dict: A dictionary of edges found between variables, where the keys are tuples representing the causal relationship between two variables,
            and the values are the strength of the relationship.
        """