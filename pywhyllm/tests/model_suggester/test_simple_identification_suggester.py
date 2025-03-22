from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_identification_suggester import SimpleIdentificationSuggester
from ...tests.model_suggester.example_variables import TEST_PAIRS as pairs
from ...tests.model_suggester.example_variables import TEST_VARIABLE_LISTS as lists

class TestSimpleIdentificationSuggester(object):

    def test_suggest_iv(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list3_expected_ivs_result"]
        expected_result = [f"<iv>{var}</iv>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_iv(lists["list3"], "smoking", "birth weight")
        assert result == lists["list3_expected_ivs_result"]

    def test_suggest_backdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list4_expected_backdoor_result"]
        expected_result = [f"<backdoor>{var}</backdoor>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_backdoor(lists["list4"], "semaglutide treatment", "cardiovascular health")
        assert result == lists["list4_expected_backdoor_result"]

    def test_suggest_frontdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list4_expected_frontdoor_result"]
        expected_result = [f"<frontdoor>{var}</frontdoor>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_frontdoor(lists["list4"], "semaglutide treatment", "cardiovascular health")
        assert result == lists["list4_expected_frontdoor_result"]