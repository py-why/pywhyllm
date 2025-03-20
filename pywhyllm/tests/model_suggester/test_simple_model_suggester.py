from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from ...tests.model_suggester.example_variables import TEST_PAIRS as pairs

class TestSimpleModelSuggester(object):

    def test_pairwise_relationship(self, mocker):
        # TODO: add support for a smaller model than gpt-4 that can be loaded locally.
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        #Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_a_cause_b_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(pairs["test_a_cause_b"][0], pairs["test_a_cause_b"][1])
        assert result == pairs["test_a_cause_b_expected_result"]

        #Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_b_cause_a_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(pairs["test_b_cause_a"][0], pairs["test_b_cause_a"][1])
        assert result == pairs["test_b_cause_a_expected_result"]

        #Given variables A and B, but LLM doesn't return a relationship, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_no_causality_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(pairs["test_no_causality"][0], pairs["test_no_causality"][1])
        assert result == pairs["test_no_causality_expected_result"]
