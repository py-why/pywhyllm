"""
Tests for ModelSuggester — the unified async causal discovery interface.

All methods are async; tests use IsolatedAsyncioTestCase so each test
runs inside its own event loop without needing asyncio.run().
"""

import unittest
from unittest.mock import AsyncMock, MagicMock

from pywhyllm.suggesters.model_suggester import ModelSuggester
from pywhyllm.suggesters.causal_graph import CausalGraph
from pywhyllm.suggesters.response_models import (
    CausalEdge,
    CausalGraphResponse,
    DomainExpertsResponse,
    DomainExpertisesResponse,
    StakeholdersResponse,
    ConfoundingFactorsResponse,
    NegativeControlsResponse,
)

VARIABLES = ["smoking", "lung_cancer", "age", "tar_deposits"]


def _make_modeler():
    """Return a ModelSuggester wired to an AsyncMock client."""
    mock_client = MagicMock()
    mock_client.chat = MagicMock()
    mock_client.chat.completions = MagicMock()
    mock_client.chat.completions.create = AsyncMock()
    return ModelSuggester(client=mock_client), mock_client


def _graph_response(*edges):
    """Build a CausalGraphResponse from (cause, effect) pairs."""
    return CausalGraphResponse(
        edges=[
            CausalEdge(cause=c, effect=e, confidence=0.9, reasoning="test reasoning")
            for c, e in edges
        ]
    )


class TestModelSuggesterGraph(unittest.IsolatedAsyncioTestCase):

    async def test_suggest_graph_no_experts(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = _graph_response(
            ("smoking", "lung_cancer"),
            ("smoking", "tar_deposits"),
        )
        graph = await modeler.suggest_graph(VARIABLES)
        self.assertIsInstance(graph, CausalGraph)
        self.assertIn(("smoking", "lung_cancer"), graph.edges)
        self.assertIn(("smoking", "tar_deposits"), graph.edges)

    async def test_suggest_graph_with_experts(self):
        modeler, mock_client = _make_modeler()
        # Two experts both suggest the same edge → votes=2
        mock_client.chat.completions.create.return_value = _graph_response(
            ("smoking", "lung_cancer"),
        )
        graph = await modeler.suggest_graph(VARIABLES, expertise_list=["oncologist", "epidemiologist"])
        self.assertIsInstance(graph, CausalGraph)
        data = graph.edge_data("smoking", "lung_cancer")
        self.assertIsNotNone(data)
        self.assertEqual(data.votes, 2)

    async def test_suggest_graph_drops_low_confidence_edges(self):
        """Edges below min_confidence (default 0.5) must not appear in the graph."""
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = CausalGraphResponse(
            edges=[
                CausalEdge(cause="smoking", effect="lung_cancer", confidence=0.9, reasoning="strong link"),
                CausalEdge(cause="lung_cancer", effect="smoking", confidence=0.03, reasoning="speculative reverse"),
            ]
        )
        graph = await modeler.suggest_graph(VARIABLES)
        self.assertIn(("smoking", "lung_cancer"), graph.edges)
        self.assertNotIn(("lung_cancer", "smoking"), graph.edges)

    async def test_suggest_graph_custom_min_confidence(self):
        """min_confidence=0.0 should let all edges through."""
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = CausalGraphResponse(
            edges=[
                CausalEdge(cause="smoking", effect="lung_cancer", confidence=0.9, reasoning="strong"),
                CausalEdge(cause="lung_cancer", effect="smoking", confidence=0.03, reasoning="weak"),
            ]
        )
        graph = await modeler.suggest_graph(VARIABLES, min_confidence=0.0)
        self.assertIn(("smoking", "lung_cancer"), graph.edges)
        self.assertIn(("lung_cancer", "smoking"), graph.edges)

    async def test_suggest_graph_parallel_calls(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = _graph_response(
            ("age", "lung_cancer"),
        )
        experts = ["oncologist", "epidemiologist", "pulmonologist"]
        graph = await modeler.suggest_graph(VARIABLES, expertise_list=experts)
        # One call per expert
        self.assertEqual(mock_client.chat.completions.create.call_count, len(experts))


class TestModelSuggesterExperts(unittest.IsolatedAsyncioTestCase):

    async def test_suggest_domain_experts(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = DomainExpertsResponse(
            experts=["oncologist", "epidemiologist", "pulmonologist", "geneticist"]
        )
        result = await modeler.suggest_domain_experts(VARIABLES, n_experts=3)
        self.assertEqual(result, ["oncologist", "epidemiologist", "pulmonologist"])

    async def test_suggest_domain_expertises(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = DomainExpertisesResponse(
            expertises=["oncology", "epidemiology", "pulmonology"]
        )
        result = await modeler.suggest_domain_expertises(VARIABLES, n_experts=3)
        self.assertEqual(result, ["oncology", "epidemiology", "pulmonology"])

    async def test_suggest_stakeholders(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = StakeholdersResponse(
            stakeholders=["patients", "researchers", "insurers"]
        )
        result = await modeler.suggest_stakeholders(VARIABLES, n_stakeholders=3)
        self.assertEqual(result, ["patients", "researchers", "insurers"])


class TestModelSuggesterConfounders(unittest.IsolatedAsyncioTestCase):

    async def test_suggest_confounders_observed(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = ConfoundingFactorsResponse(
            confounding_factors=["age"]
        )
        result = await modeler.suggest_confounders("smoking", "lung_cancer", VARIABLES)
        self.assertEqual(result, ["age"])

    async def test_suggest_confounders_filters_non_candidates(self):
        """Variables not in the candidate list should be stripped from the result."""
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = ConfoundingFactorsResponse(
            confounding_factors=["age", "invented_variable"]
        )
        result = await modeler.suggest_confounders("smoking", "lung_cancer", VARIABLES)
        self.assertIn("age", result)
        self.assertNotIn("invented_variable", result)

    async def test_suggest_confounders_latent(self):
        from pywhyllm.suggesters.response_models import LatentConfoundersResponse
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = LatentConfoundersResponse(
            confounding_factors=["socioeconomic_status", "genetic_predisposition"]
        )
        result = await modeler.suggest_confounders(
            "smoking", "lung_cancer", VARIABLES, latent=True
        )
        self.assertIn("socioeconomic_status", result)
        self.assertIn("genetic_predisposition", result)

    async def test_suggest_confounders_deduplicates_across_experts(self):
        modeler, mock_client = _make_modeler()
        # Both experts return the same confounder
        mock_client.chat.completions.create.return_value = ConfoundingFactorsResponse(
            confounding_factors=["age"]
        )
        result = await modeler.suggest_confounders(
            "smoking", "lung_cancer", VARIABLES,
            expertise_list=["oncologist", "epidemiologist"],
        )
        self.assertEqual(result.count("age"), 1)


class TestModelSuggesterNegativeControls(unittest.IsolatedAsyncioTestCase):

    async def test_suggest_negative_controls(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = NegativeControlsResponse(
            negative_controls=["age"]
        )
        result = await modeler.suggest_negative_controls("smoking", "lung_cancer", VARIABLES)
        self.assertEqual(result, ["age"])

    async def test_suggest_negative_controls_filters_non_candidates(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = NegativeControlsResponse(
            negative_controls=["age", "not_in_list"]
        )
        result = await modeler.suggest_negative_controls("smoking", "lung_cancer", VARIABLES)
        self.assertIn("age", result)
        self.assertNotIn("not_in_list", result)

    async def test_suggest_negative_controls_deduplicates_across_experts(self):
        modeler, mock_client = _make_modeler()
        mock_client.chat.completions.create.return_value = NegativeControlsResponse(
            negative_controls=["age"]
        )
        result = await modeler.suggest_negative_controls(
            "smoking", "lung_cancer", VARIABLES,
            expertise_list=["oncologist", "epidemiologist"],
        )
        self.assertEqual(result.count("age"), 1)
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)


class TestModelSuggesterTemperature(unittest.IsolatedAsyncioTestCase):

    async def test_temperature_passed_in_api_call(self):
        """When temperature is set it must appear in every create() call."""
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=CausalGraphResponse(edges=[])
        )
        modeler = ModelSuggester(client=mock_client, temperature=0.0)
        await modeler.suggest_graph(VARIABLES)
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        self.assertIn("temperature", call_kwargs)
        self.assertEqual(call_kwargs["temperature"], 0.0)

    async def test_no_temperature_omits_key(self):
        """Default (temperature=None) must NOT include temperature in the call."""
        mock_client = MagicMock()
        mock_client.chat.completions.create = AsyncMock(
            return_value=CausalGraphResponse(edges=[])
        )
        modeler = ModelSuggester(client=mock_client)
        await modeler.suggest_graph(VARIABLES)
        call_kwargs = mock_client.chat.completions.create.call_args.kwargs
        self.assertNotIn("temperature", call_kwargs)


class TestModelSuggesterValidation(unittest.IsolatedAsyncioTestCase):

    async def test_critique_graph(self):
        modeler, mock_client = _make_modeler()
        original = CausalGraph.from_responses([
            _graph_response(("smoking", "lung_cancer"), ("age", "lung_cancer"))
        ])
        # Critique confirms one edge and drops another
        mock_client.chat.completions.create.return_value = _graph_response(
            ("smoking", "lung_cancer"),
        )
        critique = await modeler.critique_graph(original, VARIABLES)
        self.assertIsInstance(critique, CausalGraph)
        self.assertIn(("smoking", "lung_cancer"), critique.edges)
        self.assertNotIn(("age", "lung_cancer"), critique.edges)

    async def test_critique_graph_with_experts(self):
        modeler, mock_client = _make_modeler()
        original = CausalGraph.from_responses([
            _graph_response(("smoking", "lung_cancer"))
        ])
        mock_client.chat.completions.create.return_value = _graph_response(
            ("smoking", "lung_cancer"),
        )
        critique = await modeler.critique_graph(
            original, VARIABLES, expertise_list=["oncologist", "epidemiologist"]
        )
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)
        self.assertIsInstance(critique, CausalGraph)

    async def test_critique_graph_min_confidence(self):
        """Edges below min_confidence should not appear in critique result."""
        modeler, mock_client = _make_modeler()
        original = CausalGraph.from_responses([_graph_response(("smoking", "lung_cancer"))])
        mock_client.chat.completions.create.return_value = CausalGraphResponse(
            edges=[
                CausalEdge(cause="smoking", effect="lung_cancer", confidence=0.9, reasoning="strong"),
                CausalEdge(cause="lung_cancer", effect="smoking", confidence=0.05, reasoning="noise"),
            ]
        )
        critique = await modeler.critique_graph(original, VARIABLES)
        self.assertIn(("smoking", "lung_cancer"), critique.edges)
        self.assertNotIn(("lung_cancer", "smoking"), critique.edges)
