import asyncio

from .causal_graph import CausalGraph
from ._prompts import critique_messages
from .response_models import CausalGraphResponse


class ValidationMixin:
    """
    Causal validation methods — critiquing an existing graph.

    Relies on ``self.client``, ``self.context``, and ``self._api_kwargs``
    provided by ``ModelSuggester.__init__``.
    """

    async def critique_graph(
        self,
        graph: CausalGraph,
        variables: list[str],
        expertise_list: list[str] | None = None,
        min_confidence: float = 0.5,
    ) -> CausalGraph:
        """
        Get a second opinion on an existing causal graph.

        Shows the LLM the original edges and asks which ones are valid
        direct causal relationships (and whether any are missing).
        Returns a new ``CausalGraph`` representing the critique's view.

        Compare with the original to find confirmed vs disputed edges::

            original = await suggester.suggest_graph(variables, experts)
            critique = await suggester.critique_graph(original, variables, experts)

            for (cause, effect) in original.edges:
                if critique.edge_data(cause, effect):
                    print(f"CONFIRMED: {cause} → {effect}")
                else:
                    print(f"DISPUTED:  {cause} → {effect}")

        Parameters
        ----------
        graph : CausalGraph
            The graph to critique.
        variables : list[str]
            The original variable list.
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel.
        min_confidence : float
            Edges below this confidence are dropped before being counted
            as a vote. Default is 0.5.

        Returns
        -------
        CausalGraph
            A new graph containing edges the critique considers valid,
            plus any new edges it suggests.
        """
        edge_block = "\n".join(
            f"  {cause} → {effect}" for (cause, effect) in graph.edges
        )

        if not expertise_list:
            response = await self._critique_call(variables, edge_block, expertise=None)
            return CausalGraph.from_responses([response], min_confidence=min_confidence)

        responses = await asyncio.gather(*[
            self._critique_call(variables, edge_block, expertise=expert)
            for expert in expertise_list
        ])
        return CausalGraph.from_responses(list(responses), min_confidence=min_confidence)

    async def _critique_call(
        self,
        variables: list[str],
        edge_block: str,
        expertise: str | None,
    ) -> CausalGraphResponse:
        return await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=CausalGraphResponse,
            messages=critique_messages(variables, edge_block, self.context, expertise),
        )
