"""
Tests for CausalGraph and EdgeData.

Covers all local query methods, edge accumulation, confidence filtering,
top_edges, reasoning_for, and the properties — zero LLM calls throughout.
"""

import unittest

from pywhyllm.suggesters.causal_graph import CausalGraph, EdgeData
from pywhyllm.suggesters.response_models import CausalEdge, CausalGraphResponse


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _resp(*edges, confidence=0.9):
    """Build a CausalGraphResponse from (cause, effect) pairs."""
    return CausalGraphResponse(
        edges=[
            CausalEdge(cause=c, effect=e, confidence=confidence, reasoning=f"{c}->{e} reasoning")
            for c, e in edges
        ]
    )


def _graph(*edges, confidence=0.9, min_confidence=0.5):
    return CausalGraph.from_responses([_resp(*edges, confidence=confidence)], min_confidence=min_confidence)


# ---------------------------------------------------------------------------
# EdgeData
# ---------------------------------------------------------------------------

class TestEdgeData(unittest.TestCase):

    def test_update_increments_votes(self):
        data = EdgeData(votes=1, avg_confidence=0.8, reasonings=["first"])
        data._update(confidence=0.6, reasoning="second")
        self.assertEqual(data.votes, 2)

    def test_update_running_average(self):
        data = EdgeData(votes=1, avg_confidence=0.8, reasonings=["first"])
        data._update(confidence=0.6, reasoning="second")
        # (0.8 * 1 + 0.6) / 2 = 0.7
        self.assertAlmostEqual(data.avg_confidence, 0.7)

    def test_update_appends_reasoning(self):
        data = EdgeData(votes=1, avg_confidence=0.9, reasonings=["first"])
        data._update(confidence=0.9, reasoning="second")
        self.assertEqual(data.reasonings, ["first", "second"])


# ---------------------------------------------------------------------------
# CausalGraph.from_responses — construction and merging
# ---------------------------------------------------------------------------

class TestCausalGraphFromResponses(unittest.TestCase):

    def test_single_response_builds_graph(self):
        graph = _graph(("A", "B"), ("B", "C"))
        self.assertIn(("A", "B"), graph.edges)
        self.assertIn(("B", "C"), graph.edges)

    def test_two_responses_merge_votes(self):
        r1 = _resp(("A", "B"))
        r2 = _resp(("A", "B"))
        graph = CausalGraph.from_responses([r1, r2])
        self.assertEqual(graph.edge_data("A", "B").votes, 2)

    def test_two_responses_average_confidence(self):
        r1 = CausalGraphResponse(edges=[CausalEdge(cause="A", effect="B", confidence=0.8, reasoning="r1")])
        r2 = CausalGraphResponse(edges=[CausalEdge(cause="A", effect="B", confidence=0.6, reasoning="r2")])
        graph = CausalGraph.from_responses([r1, r2])
        self.assertAlmostEqual(graph.edge_data("A", "B").avg_confidence, 0.7)

    def test_different_edges_from_two_responses(self):
        r1 = _resp(("A", "B"))
        r2 = _resp(("C", "D"))
        graph = CausalGraph.from_responses([r1, r2])
        self.assertEqual(graph.edge_data("A", "B").votes, 1)
        self.assertEqual(graph.edge_data("C", "D").votes, 1)

    def test_min_confidence_drops_low_edges(self):
        r = CausalGraphResponse(edges=[
            CausalEdge(cause="A", effect="B", confidence=0.9, reasoning="strong"),
            CausalEdge(cause="B", effect="A", confidence=0.2, reasoning="weak"),
        ])
        graph = CausalGraph.from_responses([r], min_confidence=0.5)
        self.assertIn(("A", "B"), graph.edges)
        self.assertNotIn(("B", "A"), graph.edges)

    def test_min_confidence_zero_keeps_all(self):
        r = CausalGraphResponse(edges=[
            CausalEdge(cause="A", effect="B", confidence=0.9, reasoning="strong"),
            CausalEdge(cause="B", effect="A", confidence=0.01, reasoning="very weak"),
        ])
        graph = CausalGraph.from_responses([r], min_confidence=0.0)
        self.assertIn(("A", "B"), graph.edges)
        self.assertIn(("B", "A"), graph.edges)

    def test_empty_responses_returns_empty_graph(self):
        graph = CausalGraph.from_responses([_resp()])
        self.assertEqual(len(graph), 0)

    def test_reasoning_stored_per_expert(self):
        r1 = CausalGraphResponse(edges=[CausalEdge(cause="A", effect="B", confidence=0.9, reasoning="expert1 says so")])
        r2 = CausalGraphResponse(edges=[CausalEdge(cause="A", effect="B", confidence=0.8, reasoning="expert2 agrees")])
        graph = CausalGraph.from_responses([r1, r2])
        reasonings = graph.reasoning_for("A", "B")
        self.assertIn("expert1 says so", reasonings)
        self.assertIn("expert2 agrees", reasonings)


# ---------------------------------------------------------------------------
# Structural queries
# ---------------------------------------------------------------------------

class TestCausalGraphQueries(unittest.TestCase):
    """
    Graph for these tests:
        A → B → D
        A → C → D
        E → B
    """

    def setUp(self):
        self.graph = _graph(
            ("A", "B"), ("A", "C"),
            ("B", "D"), ("C", "D"),
            ("E", "B"),
        )

    def test_parents_of(self):
        self.assertCountEqual(self.graph.parents_of("B"), ["A", "E"])
        self.assertCountEqual(self.graph.parents_of("D"), ["B", "C"])
        self.assertEqual(self.graph.parents_of("A"), [])

    def test_children_of(self):
        self.assertCountEqual(self.graph.children_of("A"), ["B", "C"])
        self.assertCountEqual(self.graph.children_of("B"), ["D"])
        self.assertEqual(self.graph.children_of("D"), [])

    def test_ancestors_of(self):
        ancestors = self.graph.ancestors_of("D")
        self.assertIn("A", ancestors)
        self.assertIn("B", ancestors)
        self.assertIn("C", ancestors)
        self.assertIn("E", ancestors)
        self.assertNotIn("D", ancestors)

    def test_ancestors_of_root_is_empty(self):
        self.assertEqual(self.graph.ancestors_of("A"), [])

    def test_descendants_of(self):
        descendants = self.graph.descendants_of("A")
        self.assertIn("B", descendants)
        self.assertIn("C", descendants)
        self.assertIn("D", descendants)
        self.assertNotIn("A", descendants)

    def test_descendants_of_leaf_is_empty(self):
        self.assertEqual(self.graph.descendants_of("D"), [])

    def test_mediators_of(self):
        # A → B → D  and  A → C → D  so both B and C mediate A→D
        mediators = self.graph.mediators_of("A", "D")
        self.assertIn("B", mediators)
        self.assertIn("C", mediators)

    def test_mediators_of_no_path(self):
        self.assertEqual(self.graph.mediators_of("E", "A"), [])

    def test_instrumental_variables_for(self):
        # Graph: A→B→D, A→C→D, E→B
        # IV candidates for (treatment=B, outcome=D):
        #   E → B only, no path to D without going through B → valid IV
        #   A → B and A → C → D  (A can reach D without B) → NOT an IV
        ivs = self.graph.instrumental_variables_for("B", "D")
        self.assertIn("E", ivs)
        self.assertNotIn("A", ivs)

    def test_variables_property(self):
        vars_ = self.graph.variables
        for v in ["A", "B", "C", "D", "E"]:
            self.assertIn(v, vars_)


# ---------------------------------------------------------------------------
# Edge data helpers
# ---------------------------------------------------------------------------

class TestCausalGraphEdgeHelpers(unittest.TestCase):

    def setUp(self):
        r = CausalGraphResponse(edges=[
            CausalEdge(cause="X", effect="Y", confidence=0.85, reasoning="because physics"),
        ])
        self.graph = CausalGraph.from_responses([r])

    def test_edge_data_returns_correct_metadata(self):
        data = self.graph.edge_data("X", "Y")
        self.assertIsNotNone(data)
        self.assertEqual(data.votes, 1)
        self.assertAlmostEqual(data.avg_confidence, 0.85)

    def test_edge_data_missing_edge_returns_none(self):
        self.assertIsNone(self.graph.edge_data("Y", "X"))

    def test_reasoning_for_returns_list(self):
        reasons = self.graph.reasoning_for("X", "Y")
        self.assertEqual(reasons, ["because physics"])

    def test_reasoning_for_missing_returns_none(self):
        self.assertIsNone(self.graph.reasoning_for("Y", "X"))


# ---------------------------------------------------------------------------
# top_edges
# ---------------------------------------------------------------------------

class TestCausalGraphTopEdges(unittest.TestCase):

    def setUp(self):
        r1 = _resp(("A", "B"), ("C", "D"))
        r2 = _resp(("A", "B"))          # A→B now has 2 votes
        self.graph = CausalGraph.from_responses([r1, r2])

    def test_top_edges_returns_all_by_default(self):
        self.assertEqual(len(self.graph.top_edges()), 2)

    def test_top_edges_filters_by_min_votes(self):
        edges = self.graph.top_edges(min_votes=2)
        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0][0], ("A", "B"))

    def test_top_edges_sorted_by_votes_then_confidence(self):
        edges = self.graph.top_edges()
        # A→B (2 votes) should come before C→D (1 vote)
        self.assertEqual(edges[0][0], ("A", "B"))

    def test_top_edges_returns_edge_data(self):
        (edge, data) = self.graph.top_edges()[0]
        self.assertIsInstance(data, EdgeData)
        self.assertEqual(data.votes, 2)


# ---------------------------------------------------------------------------
# Properties and dunder methods
# ---------------------------------------------------------------------------

class TestCausalGraphDunder(unittest.TestCase):

    def test_len(self):
        graph = _graph(("A", "B"), ("B", "C"))
        self.assertEqual(len(graph), 2)

    def test_repr_contains_legend(self):
        graph = _graph(("A", "B"))
        self.assertIn("A → B means A causes B", repr(graph))

    def test_repr_contains_edge(self):
        graph = _graph(("smoking", "lung_cancer"), confidence=0.9)
        r = repr(graph)
        self.assertIn("smoking → lung_cancer", r)
        self.assertIn("0.90", r)
