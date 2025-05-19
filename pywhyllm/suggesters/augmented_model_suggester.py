import logging

from .simple_model_suggester import SimpleModelSuggester
from pywhyllm.utils.data_loader import *
from pywhyllm.utils.augmented_model_suggester_utils import *


class AugmentedModelSuggester(SimpleModelSuggester):
    def __init__(self, file_path: str = 'data/causenet-precision.jsonl.bz2'):
        super().__init__()
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
        result = find_top_match_in_causenet(variable1, variable2)
        source_text = get_source_text(result)
        retriever = split_data_and_create_vectorstore_retriever
        return query_llm(source_text, variable1, variable2, retriever)
