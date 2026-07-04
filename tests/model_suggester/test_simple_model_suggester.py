"""
Tests for SimpleModelSuggester — just a backwards-compatibility shim over ModelSuggester.

Verifies that the deprecation warning fires and that the shim otherwise behaves
identically to ModelSuggester (all real functionality is inherited).
"""

import warnings
import unittest
from unittest.mock import MagicMock

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from pywhyllm.suggesters.model_suggester import ModelSuggester

_MOCK_CLIENT = MagicMock()


class TestSimpleModelSuggester(unittest.TestCase):

    def test_is_subclass_of_model_suggester(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            suggester = SimpleModelSuggester(client=_MOCK_CLIENT)
        self.assertIsInstance(suggester, ModelSuggester)

    def test_deprecation_warning_on_instantiation(self):
        with self.assertWarns(DeprecationWarning) as ctx:
            SimpleModelSuggester(client=_MOCK_CLIENT)
        self.assertIn("SimpleModelSuggester is deprecated", str(ctx.warning))

    def test_inherits_model_and_context_defaults(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            suggester = SimpleModelSuggester(client=_MOCK_CLIENT)
        self.assertEqual(suggester.model, "gpt-4o")
        self.assertEqual(suggester.context, ModelSuggester.DEFAULT_CONTEXT)

    def test_accepts_custom_model_and_context(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            suggester = SimpleModelSuggester(client=_MOCK_CLIENT, model="gpt-4o-mini", context="test domain")
        self.assertEqual(suggester.model, "gpt-4o-mini")
        self.assertEqual(suggester.context, "test domain")
