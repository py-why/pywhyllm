from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from ...tests.model_suggester.example_variables import TEST_PAIRS as pairs
from ...tests.model_suggester.example_variables import TEST_VARIABLE_LISTS as lists


class TestSimpleModelSuggester(object):

    def test_pairwise_relationship(self, mocker):
        # TODO: add support for a smaller model than gpt-4 that can be loaded locally.
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_a_cause_b_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(pairs["test_a_cause_b"][0], pairs["test_a_cause_b"][1])
        assert result == pairs["test_a_cause_b_expected_result"]

        # Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_b_cause_a_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(pairs["test_b_cause_a"][0], pairs["test_b_cause_a"][1])
        assert result == pairs["test_b_cause_a_expected_result"]

        # Given variables A and B, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_no_causality_expected_result"][2])

        result = modeler.suggest_pairwise_relationship(pairs["test_no_causality"][0], pairs["test_no_causality"][1])
        assert result == pairs["test_no_causality_expected_result"]

    def test_suggest_relationships_two_nodes(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_a_cause_b_expected_result"][2])
        expected_result = {(pairs["test_a_cause_b_expected_result"][0], pairs["test_a_cause_b_expected_result"][1]):
                               pairs["test_a_cause_b_expected_result"][2]}
        result = modeler.suggest_relationships(pairs["test_a_cause_b"])
        assert result == expected_result

        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_b_cause_a_expected_result"][2])
        expected_result = {(pairs["test_b_cause_a_expected_result"][0], pairs["test_b_cause_a_expected_result"][1]):
                               pairs["test_b_cause_a_expected_result"][2]}
        result = modeler.suggest_relationships(pairs["test_b_cause_a"])
        assert result == expected_result

        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_no_causality_expected_result"][2])
        result = modeler.suggest_relationships(pairs["test_no_causality"])
        assert len(result) == 0

    def test_suggest_relationships(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # List of three variables
        mock_llm.__getitem__ = MagicMock(side_effect=lists["list1_expected_pairwise_description"])
        result = modeler.suggest_relationships(lists["list1"])
        assert result == lists["list1_expected_result"]

        # List of four variables
        mock_llm.__getitem__ = MagicMock(side_effect=lists["list2_expected_pairwise_description"])
        result = modeler.suggest_relationships(lists["list2"])
        assert result == lists["list2_expected_result"]

    def test_suggest_confounders(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_confounders_result"]
        expected_result = [f"<conf>{var}</conf>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_confounders(lists["list1"], "season", "shark attacks")
        assert result == lists["list1_expected_confounders_result"]
