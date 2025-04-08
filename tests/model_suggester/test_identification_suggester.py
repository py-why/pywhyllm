import unittest
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.identification_suggester import IdentificationSuggester
from pywhyllm.suggesters.model_suggester import ModelSuggester
from tests.model_suggester.data_providers.identification_suggester_data_provider import *
from tests.model_suggester.data_providers.model_suggester_data_provider import *


class TestIdentificationSuggester(unittest.TestCase):
    def test_suggest_backdoor(self):
        modeler = IdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm
        mock_model_suggester = MagicMock(spec=ModelSuggester)
        modeler.model_suggester = mock_model_suggester
        mock_model_suggester.suggest_confounders = MagicMock(return_value=test_suggest_confounders_expected_results)
        result = modeler.suggest_backdoor(test_vars[0], test_vars[1], test_vars, test_domain_expertises_expected_result)
        assert result == test_suggest_confounders_expected_results

    def test_suggest_mediators(self):
        modeler = IdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_mediator_expected_response)
        result = modeler.suggest_mediators(test_vars[0], test_vars[1], test_vars, test_domain_expertises_expected_result)
        assert result == test_suggest_mediator_expected_results

    def test_suggest_ivs(self):
        modeler = IdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_ivs_expected_response)
        result = modeler.suggest_ivs(test_vars[0], test_vars[1], test_vars, test_domain_expertises_expected_result)
        assert result == test_suggest_ivs_expected_results