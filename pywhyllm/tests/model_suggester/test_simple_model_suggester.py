import unittest
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from pywhyllm.tests.model_suggester.data_providers.simple_model_suggester_data_provider import *


class TestSimpleModelSuggester(unittest.TestCase):

    def test_pairwise_relationship(self):
        # TODO: add support for a smaller model than gpt-4 that can be loaded locally.
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=test_a_cause_b_response)
        result = modeler.suggest_pairwise_relationship(test_a_cause_b[0], test_a_cause_b[1])
        assert result == test_a_cause_b_expected_result

        # Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=test_b_cause_a_response)
        result = modeler.suggest_pairwise_relationship(test_b_cause_a[0], test_b_cause_a[1])
        assert result == test_b_cause_a_expected_result

        # Given variables A and B, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=test_no_causality_response)
        result = modeler.suggest_pairwise_relationship(test_no_causality[0], test_no_causality[1])
        assert result == test_no_causality_expected_result

    def test_suggest_relationships_two_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_a_cause_b_response)
        result = modeler.suggest_relationships(test_a_cause_b)
        assert result == test_a_cause_b_expected_relationships

        mock_llm.__getitem__ = MagicMock(return_value=test_b_cause_a_response)
        result = modeler.suggest_relationships(test_b_cause_a)
        assert result == test_b_cause_a_expected_relationships

        mock_llm.__getitem__ = MagicMock(return_value=test_no_causality_response)
        result = modeler.suggest_relationships(test_no_causality)
        assert len(result) == 0

    def test_suggest_relationships_three_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # List of three variables
        mock_llm.__getitem__ = MagicMock(
            side_effect=test_three_var_response)
        result = modeler.suggest_relationships(test_three_var)
        assert result == test_three_var_expected_relationships

    def test_suggest_relationships_four_variables(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # List of four variables
        mock_llm.__getitem__ = MagicMock(
            side_effect=test_four_var_response)
        result = modeler.suggest_relationships(test_four_var)
        assert result == test_four_var_expected_relationships

    def test_suggest_confounders(self):
        modeler = SimpleModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_confounders_response)
        result = modeler.suggest_confounders(test_confounders[2:], test_confounders[0], test_confounders[1])
        assert result == test_confounders_expected_result
