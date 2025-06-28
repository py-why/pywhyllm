import logging
import re

from .simple_model_suggester import SimpleModelSuggester
from pywhyllm.utils.data_loader import download_causenet, load_causenet_json, create_causenet_dict
from pywhyllm.utils.augmented_model_suggester_utils import *


class AugmentedModelSuggester(SimpleModelSuggester):
    """
        A class that extends SimpleModelSuggester and currently provides methods for suggesting causal relationships between variables by leveraging the CauseNet dataset for Retrieval Augmented Generation (RAG).

        Methods:
        - suggest_pairwise_relationship(variable1: str, variable2: str) -> List[str]:
            Suggests the causal relationship between two variables and returns a list containing the cause, effect, and a description of the relationship.
        """

    def __init__(self, llm, file_path: str = 'data/causenet-precision.jsonl.bz2'):
        """
        Initialize the AugmentedModelSuggester with a language model and download CauseNet data.

        Args:
            llm: The language model instance to be used for querying.
            file_path (str, optional): Path to save the downloaded CauseNet JSONL file.
                                      Defaults to 'data/causenet-precision.jsonl.bz2'.
        """

        super().__init__(llm)
        self.file_path = file_path

        logging.basicConfig(level=logging.INFO)
        url = "https://groups.uni-paderborn.de/wdqa/causenet/causality-graphs/causenet-precision.jsonl.bz2"
        success = download_causenet(url, file_path)

        if success:
            print(f"File downloaded to {file_path}")
            json_data = load_causenet_json(file_path)
            self.causenet_dict = create_causenet_dict(json_data)
        else:
            print("Download failed")

    def suggest_pairwise_relationship(self, variable1: str, variable2: str):
        """
            Suggests a cause-and-effect relationship between two variables, leveraging the CauseNet dataset for Retrieval Augmented Generation (RAG).
            If a relevant causal pair is found in CauseNet, the LLM is augmented with corresponding information regarding the relationship stored
            in CauseNet. If not found, by default, the LLM will rely on its own knowledge.

            Args:
                variable1 (str): The name of the first variable.
                variable2 (str): The name of the second variable.

            Returns:
                list: A list containing the suggested cause variable, the suggested effect variable, and a description of the reasoning behind the suggestion.  If there is no relationship between the two variables, the first two elements will be None.
            """

        result = find_top_match_in_causenet(self.causenet_dict, variable1, variable2)
        if result:
            source_text = get_source_text(result)
            retriever = split_data_and_create_vectorstore_retriever(source_text)
            response = query_llm(variable1, variable2, source_text, retriever)
        else:
            response = query_llm(variable1, variable2)

        answer = re.findall(r'<answer>(.*?)</answer>', response)
        answer = [ans.strip() for ans in answer]
        answer_str = "".join(answer)

        if answer_str == "A":
            return [variable1, variable2, response]
        elif answer_str == "B":
            return [variable2, variable1, response]
        elif answer_str == "C":
            return [None, None, response]
        else:
            assert False, "Invalid answer from LLM: " + answer_str
