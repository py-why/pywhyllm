import unittest
from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.tuebingen_model_suggester import TuebingenModelSuggester, Strategy
from tests.model_suggester.data_providers.tuebingen_model_suggester_data_provider import *

class TestTuebingenModelSuggester(unittest.TestCase):
    def test_suggest_description(self):
        modeler = TuebingenModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_description_expected_response)
        result = modeler.suggest_description(variable, True)
        assert result == test_suggest_description_expected_result

    def test_suggest_onesided_relationship(self):
        modeler = TuebingenModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        #Given the two variables and their descriptions, variable a causes variable b
        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_onesided_relationship_a_cause_b_expected_response)
        result = modeler.suggest_onesided_relationship(variable_a, description_a, variable_b, description_b)
        assert result == test_suggest_onesided_relationship_a_cause_b_expected_result

        #Given the two variables and their descriptions, variable a does not cause variable b
        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_onesided_relationship_a_not_cause_b_expected_response)
        result = modeler.suggest_onesided_relationship(variable_a, description_a, variable_b, description_b)
        assert result == test_suggest_onesided_relationship_a_not_cause_b_expected_result

    def test__build_description_program(self):
        modeler = TuebingenModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm
        #Test no context, no reference
        result = modeler._build_description_program(variable, False, False)
        assert result == test__build_description_program_no_context_no_reference_expected_result
        #Test no context, with reference
        result = modeler._build_description_program(variable, False, True)
        assert result == test__build_description_program_no_context_with_reference_expected_result
        #Test with context, no reference
        result = modeler._build_description_program(variable, True, False)
        assert result == test__build_description_program_with_context_no_reference_expected_result
        #Test with context, with reference
        result = modeler._build_description_program(variable, True, True)
        assert result == test__build_description_program_with_context_with_reference_expected_result

    def test_suggest_relationship(self):
        modeler = TuebingenModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)
        #Given the two variables and their descriptions, variable a causes variable b
        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_relationship_a_cause_b_expected_response)
        result = modeler.suggest_relationship(variable_a, variable_b, description_a, description_b, domain,
                                              strategy=Strategy.ToT_Single, ask_reference=True)
        assert result == test_suggest_relationship_a_cause_b_expected_result
        #Given the two variables and their descriptions, variable a does not cause variable b
        mock_llm.__getitem__ = MagicMock(return_value=test_suggest_relationship_a_not_cause_b_expected_response)
        result = modeler.suggest_relationship(variable_a, variable_b, description_a, description_b, domain,
                                              strategy=Strategy.ToT_Single, ask_reference=True)
        assert result == test_suggest_relationship_a_not_cause_b_expected_result

    def test__build_relationship_program(self):
        modeler = TuebingenModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        result = modeler._build_relationship_program(variable_a, description_a, variable_b, description_b, domain,
                                                     use_description=False, ask_reference=False)
        assert result == test__build_relationship_program_expected_result
