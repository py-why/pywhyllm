import unittest
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_identification_suggester import SimpleIdentificationSuggester
from tests.model_suggester.data_providers.simple_identification_suggester_data_provider import *

class TestSimpleIdentificationSuggester(unittest.TestCase):

    def test_suggest_iv(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_iv_expected_response)
        result = modeler.suggest_iv(test_vars[2:], test_vars[0], test_vars[1])
        assert result == test_iv_expected_result

    def test_suggest_backdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_backdoor_expected_response)
        result = modeler.suggest_backdoor(test_vars[2:], test_vars[0], test_vars[1])
        assert result == test_backdoor_expected_result

    def test_suggest_frontdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=test_frontdoor_expected_response)
        result = modeler.suggest_frontdoor(test_vars[2:], test_vars[0], test_vars[1])
        assert result == test_frontdoor_expected_result
