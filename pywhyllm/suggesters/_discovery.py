import asyncio

from .causal_graph import CausalGraph
from ._prompts import (
    graph_messages,
    domain_experts_messages,
    domain_expertises_messages,
    stakeholders_messages,
)
from .response_models import (
    CausalGraphResponse,
    DomainExpertsResponse,
    DomainExpertisesResponse,
    StakeholdersResponse,
)


class DiscoveryMixin:
    """
    Causal discovery methods — building the graph and recommending experts.

    Relies on ``self.client``, ``self.model``, ``self.context``, and
    ``self._api_kwargs`` provided by ``ModelSuggester.__init__``.
    """

    async def suggest_graph(
        self,
        variables: list[str],
        expertise_list: list[str] | None = None,
        min_confidence: float = 0.5,
    ) -> CausalGraph:
        """
        Build a causal graph over `variables`.

        Without experts: one LLM call with a generic causal reasoning persona.
        With experts: one call per expert fired in parallel; edges are merged
        by vote count so you can filter by consensus strength.

        Parameters
        ----------
        variables : list[str]
            Variable names to reason over.
        expertise_list : list[str] | None
            Domain expert roles (e.g. ``["cardiologist", "epidemiologist"]``).
            ``None`` uses a generic persona (cheaper, fewer calls).
        min_confidence : float
            Edges with confidence below this threshold are dropped before
            being counted as a vote. Default is 0.5.

        Returns
        -------
        CausalGraph
            Local graph object — query parents, children, ancestors, etc.
            with no further LLM calls.
        """
        if not expertise_list:
            response = await self._graph_call(variables, expertise=None)
            return CausalGraph.from_responses([response], min_confidence=min_confidence)

        responses = await asyncio.gather(*[
            self._graph_call(variables, expertise=expert)
            for expert in expertise_list
        ])
        return CausalGraph.from_responses(list(responses), min_confidence=min_confidence)

    async def _graph_call(
        self,
        variables: list[str],
        expertise: str | None,
    ) -> CausalGraphResponse:
        return await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=CausalGraphResponse,
            messages=graph_messages(variables, self.context, expertise),
        )

    # ------------------------------------------------------------------
    # Expert / stakeholder discovery
    # ------------------------------------------------------------------

    async def suggest_domain_experts(
        self,
        variables: list[str],
        n_experts: int = 3,
    ) -> list[str]:
        """Suggest domain expert roles relevant to causal reasoning over `variables`."""
        response = await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=DomainExpertsResponse,
            messages=domain_experts_messages(variables, n_experts),
        )
        return response.experts[:n_experts]

    async def suggest_domain_expertises(
        self,
        variables: list[str],
        n_experts: int = 3,
    ) -> list[str]:
        """Suggest domain expertise areas relevant to causal reasoning over `variables`."""
        response = await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=DomainExpertisesResponse,
            messages=domain_expertises_messages(variables, n_experts),
        )
        return response.expertises[:n_experts]

    async def suggest_stakeholders(
        self,
        variables: list[str],
        n_stakeholders: int = 5,
    ) -> list[str]:
        """Suggest stakeholders relevant to causal reasoning over `variables`."""
        response = await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=StakeholdersResponse,
            messages=stakeholders_messages(variables, n_stakeholders),
        )
        return response.stakeholders[:n_stakeholders]
