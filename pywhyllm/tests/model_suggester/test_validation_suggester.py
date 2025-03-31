import unittest
from typing import Dict
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.validation_suggester import ValidationSuggester
from pywhyllm.tests.model_suggester.data_providers.validation_suggester_data_provider import *
from pywhyllm.tests.model_suggester.data_providers.model_suggester_data_provider import *
from pywhyllm.helpers import RelationshipStrategy


class TestValidationSuggester(unittest.TestCase):
    def test_suggest_latent_confounders(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_latent_confounders_expected_response)

        result = modeler.suggest_latent_confounders(test_vars[0], test_vars[1], domain_expertises)

        assert result == test_suggest_latent_confounders_expected_results

    def test_request_latent_confounders(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_latent_confounders_expected_response)

        latent_confounders_counter: Dict[str, int] = dict()
        result = modeler.request_latent_confounders(test_vars[0], test_vars[1], latent_confounders_counter,
                                                    domain_expertises[0])

        assert result == test_request_latent_confounders_expected_results

    def test_suggest_negative_controls(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_negative_controls_expected_response)

        result = modeler.suggest_negative_controls(test_vars[0], test_vars[1], test_vars, domain_expertises)

        assert result == test_suggest_negative_controls_expected_results

    def test_request_negative_controls(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_negative_controls_expected_response)

        negative_controls_counter: Dict[str, int] = dict()
        result = modeler.request_negative_controls(test_vars[0], test_vars[1], test_vars, negative_controls_counter,
                                                   domain_expertises[0])

        assert result == test_request_negative_controls_expected_results

    def test_request_parent_critique(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_parent_critique_expected_response)

        result = modeler.request_parent_critique(test_vars[0], test_vars, domain_expertises[0])

        assert result == test_parent_critique_expected_results

    def test_request_children_critique(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_children_critique_expected_response)

        result = modeler.request_children_critique(test_vars[0], test_vars, domain_expertises[0])

        assert result == test_children_critique_expected_results

    def test_request_pairwise_critique(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        mock_llm.__getitem__ = MagicMock(return_value=test_pairwise_critique_expected_response)
        result = modeler.request_pairwise_critique(domain_expertises[0], test_vars[0], test_vars[1])
        assert result == test_pairwise_critique_expected_results

    def test_critique_graph(self):
        modeler = ValidationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        # parent
        mock_llm.__getitem__ = MagicMock(side_effect=test_critique_graph_parent_expected_response)
        result = modeler.critique_graph(test_vars, test_suggest_relationships_parent_expected_results,
                                        domain_expertises, RelationshipStrategy.Parent)

        assert result == test_critique_graph_parent_expected_results

        mock_llm.__getitem__ = MagicMock(side_effect=test_critique_graph_children_expected_response)
        result = modeler.critique_graph(test_vars, test_suggest_relationships_child_expected_results,
                                        domain_expertises, RelationshipStrategy.Child)

        assert result == test_critique_graph_children_expected_results

        mock_llm.__getitem__ = MagicMock(side_effect=test_critique_graph_pairwise_expected_response)
        result = modeler.critique_graph(test_vars, test_suggest_relationships_pairwise_expected_results,
                                        domain_expertises, RelationshipStrategy.Pairwise)
        assert result == test_critique_graph_pairwise_expected_results
