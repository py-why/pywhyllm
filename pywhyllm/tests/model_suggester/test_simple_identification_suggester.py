from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.simple_identification_suggester import SimpleIdentificationSuggester
from ...tests.model_suggester.tests_input import TESTS_SIMPLE_IDENTIFICATION_SUGGESTER as inputs
from ...tests.model_suggester.tests_expected_results import \
    EXPECTED_RESULTS_SIMPLE_IDENTIFICATION_SUGGESTER as expected_results


class TestSimpleIdentificationSuggester(object):

    def test_suggest_iv(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = expected_results["test_var_list_expected_ivs"][0]
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_iv(inputs["test_var_list"][2:], inputs["test_var_list"][0], inputs["test_var_list"][1])
        assert result == expected_results["test_var_list_expected_ivs"][1]

    def test_suggest_backdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = expected_results["test_var_list_expected_backdoors"][0]
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_backdoor(inputs["test_var_list"][2:], inputs["test_var_list"][0], inputs["test_var_list"][1])
        assert result == expected_results["test_var_list_expected_backdoors"][1]

    def test_suggest_frontdoor(self):
        modeler = SimpleIdentificationSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = expected_results["test_var_list_expected_frontdoors"][0]
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_frontdoor(inputs["test_var_list"][2:], inputs["test_var_list"][0], inputs["test_var_list"][1])
        assert result == expected_results["test_var_list_expected_frontdoors"][1]
