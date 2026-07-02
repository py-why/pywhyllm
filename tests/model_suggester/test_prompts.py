"""
Tests for _prompts.py — the prompt builder module.

Verifies structure (correct roles, non-empty content) and that key
parameters are interpolated into the right messages.  No LLM calls.
"""

import unittest

from pywhyllm.suggesters._prompts import (
    graph_messages,
    domain_experts_messages,
    domain_expertises_messages,
    stakeholders_messages,
    confounders_messages,
    latent_confounders_messages,
    negative_controls_messages,
    critique_messages,
)

VARIABLES = ["smoking", "lung_cancer", "age"]
CONTEXT = "cardiovascular health"
EXPERTISE = "oncology"


def _assert_message_structure(test, messages):
    """All builders must return [system, user] with non-empty content."""
    test.assertEqual(len(messages), 2)
    test.assertEqual(messages[0]["role"], "system")
    test.assertEqual(messages[1]["role"], "user")
    test.assertTrue(messages[0]["content"].strip())
    test.assertTrue(messages[1]["content"].strip())


class TestGraphMessages(unittest.TestCase):

    def test_structure(self):
        _assert_message_structure(self, graph_messages(VARIABLES, CONTEXT, EXPERTISE))

    def test_expertise_injected_into_system(self):
        msgs = graph_messages(VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn(EXPERTISE, msgs[0]["content"])
        self.assertIn(CONTEXT, msgs[0]["content"])

    def test_no_expertise_uses_generic_system(self):
        msgs = graph_messages(VARIABLES, CONTEXT, expertise=None)
        self.assertIn(CONTEXT, msgs[0]["content"])
        self.assertNotIn("expert in", msgs[0]["content"])

    def test_variables_in_user_message(self):
        msgs = graph_messages(VARIABLES, CONTEXT, EXPERTISE)
        user = msgs[1]["content"]
        for v in VARIABLES:
            self.assertIn(v, user)

    def test_user_asks_for_direct_causal_relationships(self):
        msgs = graph_messages(VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn("direct causal", msgs[1]["content"].lower())


class TestDomainExpertMessages(unittest.TestCase):

    def test_experts_structure(self):
        _assert_message_structure(self, domain_experts_messages(VARIABLES, n_experts=3))

    def test_n_experts_in_user_message(self):
        msgs = domain_experts_messages(VARIABLES, n_experts=5)
        self.assertIn("5", msgs[1]["content"])

    def test_expertises_structure(self):
        _assert_message_structure(self, domain_expertises_messages(VARIABLES, n_experts=3))

    def test_stakeholders_structure(self):
        _assert_message_structure(self, stakeholders_messages(VARIABLES, n_stakeholders=4))

    def test_n_stakeholders_in_user_message(self):
        msgs = stakeholders_messages(VARIABLES, n_stakeholders=4)
        self.assertIn("4", msgs[1]["content"])


class TestConfoundersMessages(unittest.TestCase):

    def test_observed_structure(self):
        _assert_message_structure(
            self, confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        )

    def test_treatment_and_outcome_in_user(self):
        msgs = confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn("smoking", msgs[1]["content"])
        self.assertIn("lung_cancer", msgs[1]["content"])

    def test_candidates_in_user(self):
        msgs = confounders_messages("smoking", "lung_cancer", ["age", "stress"], CONTEXT, EXPERTISE)
        self.assertIn("age", msgs[1]["content"])

    def test_no_expertise_uses_generic_system(self):
        msgs = confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, expertise=None)
        self.assertNotIn("expert in", msgs[0]["content"])

    def test_latent_structure(self):
        _assert_message_structure(
            self, latent_confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        )

    def test_latent_mentions_unmeasured(self):
        msgs = latent_confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn("latent", msgs[1]["content"].lower())

    def test_latent_lists_existing_variables_to_exclude(self):
        msgs = latent_confounders_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        for v in VARIABLES:
            self.assertIn(v, msgs[1]["content"])


class TestNegativeControlsMessages(unittest.TestCase):

    def test_structure(self):
        _assert_message_structure(
            self, negative_controls_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        )

    def test_treatment_and_outcome_in_user(self):
        msgs = negative_controls_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn("smoking", msgs[1]["content"])
        self.assertIn("lung_cancer", msgs[1]["content"])

    def test_zero_treatment_effect_language(self):
        msgs = negative_controls_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, EXPERTISE)
        self.assertIn("zero treatment effect", msgs[1]["content"].lower())

    def test_no_expertise_uses_generic_system(self):
        msgs = negative_controls_messages("smoking", "lung_cancer", VARIABLES, CONTEXT, expertise=None)
        self.assertNotIn("expert in", msgs[0]["content"])


class TestCritiqueMessages(unittest.TestCase):

    EDGE_BLOCK = "  smoking → lung_cancer\n  age → lung_cancer"

    def test_structure(self):
        _assert_message_structure(
            self, critique_messages(VARIABLES, self.EDGE_BLOCK, CONTEXT, EXPERTISE)
        )

    def test_expertise_in_system(self):
        msgs = critique_messages(VARIABLES, self.EDGE_BLOCK, CONTEXT, EXPERTISE)
        self.assertIn(EXPERTISE, msgs[0]["content"])

    def test_no_expertise_uses_generic_system(self):
        msgs = critique_messages(VARIABLES, self.EDGE_BLOCK, CONTEXT, expertise=None)
        self.assertNotIn("expert in", msgs[0]["content"])

    def test_edge_block_in_user(self):
        msgs = critique_messages(VARIABLES, self.EDGE_BLOCK, CONTEXT, EXPERTISE)
        self.assertIn(self.EDGE_BLOCK, msgs[1]["content"])

    def test_variables_in_user(self):
        msgs = critique_messages(VARIABLES, self.EDGE_BLOCK, CONTEXT, EXPERTISE)
        for v in VARIABLES:
            self.assertIn(v, msgs[1]["content"])
