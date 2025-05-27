import logging
import re

from .simple_model_suggester import SimpleModelSuggester
from pywhyllm.utils.data_loader import *
from pywhyllm.utils.augmented_model_suggester_utils import *


class AugmentedModelSuggester(SimpleModelSuggester):
    def __init__(self, llm, file_path: str = 'data/causenet-precision.jsonl.bz2'):
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
