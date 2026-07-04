from collections import deque
from dataclasses import dataclass, field

from .response_models import CausalGraphResponse


@dataclass
class EdgeData:
    """
    Metadata stored for each causal edge.

    Attributes
    ----------
    votes : int
        Number of experts (or LLM calls) that identified this edge.
    avg_confidence : float
        Running average of confidence scores across all votes.
    reasonings : list[str]
        One reasoning string per expert who identified this edge.
        Preserves the order in which experts were queried.
    """

    votes: int
    avg_confidence: float
    reasonings: list[str] = field(default_factory=list)

    def _update(self, confidence: float, reasoning: str) -> None:
        """Accumulate a new expert vote onto this edge."""
        self.avg_confidence = (
            (self.avg_confidence * self.votes) + confidence
        ) / (self.votes + 1)
        self.votes += 1
        self.reasonings.append(reasoning)


class CausalGraph:
    """
    A causal graph built from one or more LLM responses.

    All query methods are local — no LLM calls.
    Each edge stores vote count, average confidence, and the full list of
    expert reasonings so users can inspect *why* each edge was suggested.

    Attributes
    ----------
    edges : dict[tuple[str, str], EdgeData]
        Mapping of (cause, effect) → EdgeData.

    Examples
    --------
    ::

        graph = await suggester.suggest_graph(variables, expertise_list=experts)

        # Structural queries
        graph.parents_of("lung_cancer")
        graph.mediators_of("smoking", "lung_cancer")

        # Inspect reasoning for a specific edge
        graph.reasoning_for("smoking", "lung_cancer")
        graph.edge_data("smoking", "lung_cancer")
    """

    def __init__(self, edges: dict[tuple[str, str], EdgeData]):
        self._edges = edges

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    @classmethod
    def from_responses(
        cls,
        responses: list[CausalGraphResponse],
        min_confidence: float = 0.5,
    ) -> "CausalGraph":
        """
        Merge one or more CausalGraphResponses into a single graph.

        Each unique (cause, effect) pair accumulates votes, a running
        average confidence, and all expert reasoning strings.

        Parameters
        ----------
        responses : list[CausalGraphResponse]
            One response per LLM call (one per expert, or a single call
            when no experts are specified).
        min_confidence : float
            Edges with confidence below this threshold are ignored
            *per expert call* — a low-confidence suggestion from one
            expert doesn't count as a vote. Default is 0.5.
        """
        edges: dict[tuple[str, str], EdgeData] = {}
        for response in responses:
            for edge in response.edges:
                if edge.confidence < min_confidence:
                    continue
                key = (edge.cause, edge.effect)
                if key in edges:
                    edges[key]._update(edge.confidence, edge.reasoning)
                else:
                    edges[key] = EdgeData(
                        votes=1,
                        avg_confidence=edge.confidence,
                        reasonings=[edge.reasoning],
                    )
        return cls(edges)

    # ------------------------------------------------------------------
    # Structural queries — zero LLM calls
    # ------------------------------------------------------------------

    def parents_of(self, variable: str) -> list[str]:
        """Return all direct causes of `variable`."""
        return [cause for (cause, effect) in self._edges if effect == variable]

    def children_of(self, variable: str) -> list[str]:
        """Return all direct effects of `variable`."""
        return [effect for (cause, effect) in self._edges if cause == variable]

    def ancestors_of(self, variable: str) -> list[str]:
        """Return all ancestors of `variable` (transitive causes)."""
        visited: set[str] = set()
        queue = deque(self.parents_of(variable))
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                queue.extend(self.parents_of(node))
        return list(visited)

    def descendants_of(self, variable: str) -> list[str]:
        """Return all descendants of `variable` (transitive effects)."""
        visited: set[str] = set()
        queue = deque(self.children_of(variable))
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                queue.extend(self.children_of(node))
        return list(visited)

    def mediators_of(self, treatment: str, outcome: str) -> list[str]:
        """
        Return variables on the causal pathway treatment → M → outcome.

        A mediator is any variable that is both a descendant of `treatment`
        and an ancestor of `outcome`.
        """
        return list(
            set(self.descendants_of(treatment)) & set(self.ancestors_of(outcome))
        )

    def instrumental_variables_for(self, treatment: str, outcome: str) -> list[str]:
        """
        Return candidate instrumental variables for the treatment → outcome effect.

        An IV is a parent of ``treatment`` whose only path to ``outcome`` runs
        *through* ``treatment`` — i.e. it cannot reach ``outcome`` if we block
        the treatment node.

        This is a stricter (and more correct) check than simply excluding all
        ancestors of ``outcome``: a variable like E in ``E → treatment → outcome``
        is a valid IV even though it is technically an ancestor of ``outcome``.
        """
        treatment_parents = set(self.parents_of(treatment))

        # Find ancestors of outcome when treatment is removed from the graph
        ancestors_without_treatment: set[str] = set()
        queue = deque(self.parents_of(outcome))
        while queue:
            node = queue.popleft()
            if node == treatment or node in ancestors_without_treatment:
                continue
            ancestors_without_treatment.add(node)
            queue.extend(self.parents_of(node))

        return list(treatment_parents - ancestors_without_treatment)

    # ------------------------------------------------------------------
    # Edge data and reasoning queries
    # ------------------------------------------------------------------

    def edge_data(self, cause: str, effect: str) -> EdgeData | None:
        """
        Return full EdgeData for a specific edge, or None if it doesn't exist.

        EdgeData contains vote count, average confidence, and all reasonings.
        """
        return self._edges.get((cause, effect))

    def reasoning_for(self, cause: str, effect: str) -> list[str] | None:
        """
        Return all expert reasoning strings for a specific edge.

        Returns None if the edge does not exist in the graph.

        Example
        -------
        ::

            reasons = graph.reasoning_for("smoking", "lung_cancer")
            for i, r in enumerate(reasons):
                print(f"Expert {i + 1}: {r}")
        """
        data = self._edges.get((cause, effect))
        return data.reasonings if data else None

    def top_edges(self, min_votes: int = 1) -> list[tuple[tuple[str, str], EdgeData]]:
        """
        Return edges with at least `min_votes` expert agreements.

        Sorted by vote count descending, then average confidence descending.
        """
        filtered = [
            (edge, data)
            for edge, data in self._edges.items()
            if data.votes >= min_votes
        ]
        return sorted(
            filtered,
            key=lambda x: (-x[1].votes, -x[1].avg_confidence),
        )

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def edges(self) -> dict[tuple[str, str], EdgeData]:
        """Raw edge dict: (cause, effect) → EdgeData."""
        return self._edges

    @property
    def variables(self) -> list[str]:
        """All variables that appear in at least one edge."""
        seen: set[str] = set()
        for cause, effect in self._edges:
            seen.add(cause)
            seen.add(effect)
        return list(seen)

    # ------------------------------------------------------------------
    # Dunder
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Visualisation
    # ------------------------------------------------------------------

    def plot(
        self,
        min_votes: int = 1,
        rankdir: str = "LR",
        filename: str | None = None,
        format: str = "png",
    ):
        """
        Render the causal graph using Graphviz's ``dot`` layout engine.

        The ``dot`` engine is designed for DAGs — it topologically sorts
        nodes into ranks so causal direction reads naturally left-to-right
        (or top-to-bottom with ``rankdir="TB"``).

        Edge thickness and colour both encode average confidence:

        * **Dark blue, thick** — high confidence (≥ 0.8)
        * **Steel blue, medium** — moderate confidence (≥ 0.6)
        * **Light grey, thin** — lower confidence (≥ ``min_confidence`` threshold)

        When multiple experts were used, the vote count is shown as an edge
        label so you can see consensus strength at a glance.

        Parameters
        ----------
        min_votes : int
            Only plot edges with at least this many expert votes. Default 1.
        rankdir : str
            Direction of graph layout. ``"LR"`` (left → right, default) or
            ``"TB"`` (top → bottom).
        filename : str | None
            If provided, render to this path (extension added automatically).
            ``None`` returns the Digraph object for inline Jupyter display.
        format : str
            Output format when ``filename`` is set, e.g. ``"png"``, ``"svg"``,
            ``"pdf"``. Default ``"png"``.

        Returns
        -------
        graphviz.Digraph
            The Digraph object. In a Jupyter notebook this renders inline
            automatically. Call ``.render()`` on it to save to disk.

        Raises
        ------
        ImportError
            If the ``graphviz`` Python package is not installed.

        Examples
        --------
        ::

            graph.plot()                            # inline in Jupyter
            graph.plot(min_votes=2)                 # consensus edges only
            graph.plot(rankdir="TB")                # top-to-bottom layout
            graph.plot(filename="sea_ice_graph")    # save to PNG
        """
        try:
            import graphviz as gv
        except ImportError as exc:
            raise ImportError(
                "graphviz Python package is not installed.\n"
                "  pip install graphviz"
            ) from exc

        import shutil
        if shutil.which("dot") is None:
            raise RuntimeError(
                "Graphviz system binaries not found — the 'dot' executable must be on your PATH.\n"
                "  macOS:  brew install graphviz\n"
                "  Linux:  sudo apt-get install graphviz\n"
                "  Windows: https://graphviz.org/download/"
            )

        dot = gv.Digraph(engine="dot")
        dot.attr(
            rankdir=rankdir,
            fontname="Helvetica",
            bgcolor="white",
            pad="0.4",
            nodesep="0.5",
            ranksep="0.8",
        )
        dot.attr(
            "node",
            shape="box",
            style="filled,rounded",
            fillcolor="#EBF4FB",
            color="#2980B9",
            fontname="Helvetica",
            fontsize="11",
            margin="0.2,0.1",
        )
        dot.attr(
            "edge",
            fontname="Helvetica",
            fontsize="9",
            arrowsize="0.7",
        )

        edges_to_plot = [
            (edge, data)
            for edge, data in self._edges.items()
            if data.votes >= min_votes
        ]

        if not edges_to_plot:
            # Empty graph — add a placeholder node so it renders
            dot.node("(no edges)", shape="plaintext")
            return dot

        # Collect all variable names and add nodes
        variables: set[str] = set()
        for (cause, effect), _ in edges_to_plot:
            variables.add(cause)
            variables.add(effect)

        for var in variables:
            label = var.replace("_", " ")
            dot.node(var, label=label)

        # Determine whether this is a multi-expert graph
        max_votes = max(data.votes for _, data in edges_to_plot)
        show_votes = max_votes > 1

        for (cause, effect), data in edges_to_plot:
            c = data.avg_confidence

            # Colour: dark blue → steel blue → light grey as confidence drops
            if c >= 0.8:
                color = "#1A5276"
            elif c >= 0.6:
                color = "#2E86C1"
            else:
                color = "#AEB6BF"

            # Thickness: 1.0 → 3.5 scaled by confidence
            penwidth = str(round(1.0 + c * 2.5, 1))

            # Label: confidence % + vote count when using experts
            if show_votes:
                label = f" {data.votes}v / {c:.0%} "
            else:
                label = f" {c:.0%} "

            dot.edge(
                cause,
                effect,
                label=label,
                color=color,
                penwidth=penwidth,
                fontcolor="#555555",
            )

        if filename:
            dot.render(filename, format=format, cleanup=True)

        return dot

    def __repr__(self) -> str:
        lines = [
            f"CausalGraph ({len(self._edges)} edges):",
            f"  (A → B means A causes B)",
        ]
        for (cause, effect), data in sorted(
            self._edges.items(),
            key=lambda x: (-x[1].votes, -x[1].avg_confidence),
        ):
            lines.append(
                f"  {cause} → {effect}  "
                f"(votes: {data.votes}, confidence: {data.avg_confidence:.2f})"
            )
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._edges)
