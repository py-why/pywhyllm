from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from ...tests.model_suggester.tests_input import TESTS_SIMPLE_MODEL_SUGGESTER as inputs
from ...tests.model_suggester.tests_expected_results import EXPECTED_RESULTS_SIMPLE_MODEL_SUGGESTER as expected_results


class TestSimpleModelSuggester(object):

    def test_pairwise_relationship(self):
        # TODO: add support for a smaller model than gpt-4 that can be loaded locally.
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_a_cause_b_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(inputs["test_a_cause_b"][0], inputs["test_a_cause_b"][1])
        assert result == expected_results["test_a_cause_b_expected_result"]

        # Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_b_cause_a_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(inputs["test_b_cause_a"][0], inputs["test_b_cause_a"][1])
        assert result == expected_results["test_b_cause_a_expected_result"]

        # Given variables A and B, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_no_causality_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(inputs["test_no_causality"][0], inputs["test_no_causality"][1])
        assert result == expected_results["test_no_causality_expected_result"]

    def test_suggest_relationships_two_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_a_cause_b_expected_result"][2])
        result = modeler.suggest_relationships(inputs["test_a_cause_b"])
        assert result == expected_results["test_a_cause_b_expected_relationships"]

        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_b_cause_a_expected_result"][2])
        result = modeler.suggest_relationships(inputs["test_b_cause_a"])
        assert result == expected_results["test_b_cause_a_expected_relationships"]

        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_no_causality_expected_result"][2])
        result = modeler.suggest_relationships(inputs["test_no_causality"])
        assert len(result) == 0

    def test_suggest_relationships_three_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # List of three variables
        mock_llm.__getitem__ = MagicMock(
            side_effect=expected_results["test_three_var_list_expected_pairwise_descriptions"])
        result = modeler.suggest_relationships(inputs["test_three_var_list"])
        assert result == expected_results["test_three_var_list_expected_relationships"]

    def test_suggest_relationships_four_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # List of four variables
        mock_llm.__getitem__ = MagicMock(
            side_effect=expected_results["test_four_var_list_expected_pairwise_descriptions"])
        result = modeler.suggest_relationships(inputs["test_four_var_list"])
        assert result == expected_results["test_four_var_list_expected_relationships"]

    def test_suggest_confounders(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = expected_results["test_confounders_expected_result"][0]
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_confounders(inputs["test_confounders"][0], inputs["test_confounders"][1],
                                             inputs["test_confounders"][2:])
        assert result == expected_results["test_confounders_expected_result"][1]
