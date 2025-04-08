import unittest
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.model_suggester import ModelSuggester
from pywhyllm.helpers import RelationshipStrategy
from tests.model_suggester.data_providers.model_suggester_data_provider import *


class TestModelSuggester(unittest.TestCase):

    def test_suggest_domain_expertises(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_domain_expertises_expected_response)
        result = modeler.suggest_domain_expertises(test_vars)
        assert result == test_domain_expertises_expected_result

    def test_suggest_domain_experts(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_domain_experts_expected_response)
        result = modeler.suggest_domain_experts(test_vars)
        assert result == test_domain_experts_expected_result

    def test_suggest_stakeholders(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_stakeholders_expected_response)
        result = modeler.suggest_stakeholders(test_vars)
        assert result == test_stakeholders_expected_results

    # by extension, tests request_confounders
    def test_suggest_confounders(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_request_confounders_expected_response)
        result = modeler.suggest_confounders(test_vars[0], test_vars[1], test_vars,
                                             test_domain_expertises_expected_result)
        assert result == test_suggest_confounders_expected_results

    def test_suggest_parents(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_parents_expected_response)
        result = modeler.suggest_parents(test_domain_expertises_expected_result[0], test_vars[0],
                                         test_vars)
        assert result == test_parents_expected_results

    def test_suggest_children(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_children_expected_response)
        result = modeler.suggest_children(test_domain_expertises_expected_result[0], test_vars[0],
                                          test_vars)
        assert result == test_children_expected_results

    def test_suggest_pairwise_relationship(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=test_pairwise_a_cause_b_expected_response)
        result = modeler.suggest_pairwise_relationship(test_domain_expertises_expected_response[0],
                                                       test_vars[0], test_vars[1])
        assert result == test_a_cause_b_expected_results

        # Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=test_pairwise_b_cause_a_expected_response)
        result = modeler.suggest_pairwise_relationship(test_domain_expertises_expected_response[0],
                                                       test_vars[0], test_vars[1])
        assert result == test_b_cause_a_expected_results

        # Given variables A and B, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=test_pairwise_no_causality_expected_response)
        result = modeler.suggest_pairwise_relationship(test_domain_expertises_expected_response[0],
                                                       test_vars[0], test_vars[1])
        assert result == test_no_causality_expected_results

    def test_suggest_relationships(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        #parent
        mock_llm.__getitem__ = MagicMock(side_effect=test_suggest_relationships_parent_expected_response)
        result = modeler.suggest_relationships(test_vars[0], test_vars[1], test_vars, test_domain_expertises_expected_result, RelationshipStrategy.Parent)
        assert result == test_suggest_relationships_parent_expected_results
        #child
        mock_llm.__getitem__ = MagicMock(side_effect=test_suggest_relationships_child_expected_response)
        result = modeler.suggest_relationships(test_vars[0], test_vars[1], test_vars,
                                               test_domain_expertises_expected_result, RelationshipStrategy.Child)
        assert result == test_suggest_relationships_child_expected_results
        #pairwise
        mock_llm.__getitem__ = MagicMock(side_effect=tests_suggest_relationships_pairwise_expected_response)
        result = modeler.suggest_relationships(test_vars[0], test_vars[1], test_vars,
                                               test_domain_expertises_expected_result, RelationshipStrategy.Pairwise)
        assert result == test_suggest_relationships_pairwise_expected_results
        #confounder
        mock_llm.__getitem__ = MagicMock(return_value=test_request_confounders_expected_response)
        result = modeler.suggest_relationships(test_vars[0], test_vars[1], test_vars,
                                             test_domain_expertises_expected_result, RelationshipStrategy.Confounder)
        assert result == test_suggest_relationships_confounders_expected_results