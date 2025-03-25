from unittest.mock import MagicMock
from guidance.models._openai import OpenAI

from pywhyllm.suggesters.model_suggester import ModelSuggester


class TestModelSuggester(object):

    def test_suggest_domain_expertises(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        mock_llm.__getitem__ = MagicMock(return_value=expected_results["test_var_list_expected_domain_expertises"][0])
        result = modeler.suggest_domain_expertises(inputs["test_var_list"])
        assert result == expected_results["test_var_list_expected_domain_expertises"][1]

    def test_suggest_domain_experts(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_domain_experts"]
        expected_result = [f"<domain_expert>{var}</domain_expert>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_domain_experts(lists["list1"])
        assert result == lists["list1_expected_domain_experts"]

    def test_suggest_stakeholders(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_stakeholders"]
        expected_result = [f"<stakeholder>{var}</stakeholder>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_stakeholders(lists["list1"])
        assert result == lists["list1_expected_stakeholders"]

    def test_suggest_stakeholders(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_stakeholders"]
        expected_result = [f"<stakeholder>{var}</stakeholder>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_stakeholders(lists["list1"])
        assert result == lists["list1_expected_stakeholders"]

    # TODO: add suggest_confounders and request_confounders

    def test_suggest_parents(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_parents"]
        expected_result = [f"<influencing_factor>{var}</influencing_factor>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_parents(lists["list1_expected_domain_expertises"][0], "ice cream sales",
                                         lists["list1"])
        assert result == lists["list1_expected_parents"]

    def test_suggest_children(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        expected_result = lists["list1_expected_children"]
        expected_result = [f"<influenced_factor>{var}</influenced_factor>" for var in expected_result]
        expected_result = " ".join(expected_result)
        mock_llm.__getitem__ = MagicMock(return_value=expected_result)
        result = modeler.suggest_children(lists["list1_expected_domain_expertises"][0], "ice cream sales",
                                          lists["list1"])
        assert result == lists["list1_expected_children"]

    def test_suggest_pairwise_relationship(self):
        modeler = ModelSuggester()
        mock_llm = MagicMock(spec=OpenAI)
        modeler.llm = mock_llm

        mock_llm.__add__ = MagicMock(return_value=mock_llm)

        # Given variables A and B, mock the LLM to return A->B
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_a_cause_b_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(lists["list1_expected_domain_expertises"][0],
                                                       pairs["test_a_cause_b"][0], pairs["test_a_cause_b"][1])
        assert result == pairs["test_a_cause_b_expected_result"][0:2]

        # Given variables B and A, mock the LLM to return B->A
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_b_cause_a_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(lists["list1_expected_domain_expertises"][0],
                                                       pairs["test_b_cause_a"][0], pairs["test_b_cause_a"][1])
        assert result == pairs["test_b_cause_a_expected_result"][0:2]

        # Given variables A and B, mock the LLM to return no causality
        mock_llm.__getitem__ = MagicMock(return_value=pairs["test_no_causality_expected_result"][2])
        result = modeler.suggest_pairwise_relationship(lists["list1_expected_domain_expertises"][0],
                                                       pairs["test_no_causality"][0], pairs["test_no_causality"][1])
        assert result == pairs["test_no_causality_expected_result"][0]

    # TODO test_suggest_relationships
