from typing import Protocol


class ModelerProtocol(Protocol):

    async def suggest_graph(
        self,
        variables: list[str],
        expertise_list: list[str] | None = None,
    ):
        """
        Build a causal graph over `variables`.

        Parameters
        ----------
        variables : list[str]
            Variable names to reason over.
        expertise_list : list[str] | None
            Domain expert roles for consensus. None uses a generic persona.

        Returns
        -------
        CausalGraph
        """
        ...

    async def suggest_confounders(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise_list: list[str] | None = None,
        latent: bool = False,
    ) -> list[str]:
        """
        Suggest confounders of the treatment → outcome relationship.

        Parameters
        ----------
        latent : bool
            False: search within variables. True: search outside variables.
        """
        ...

    async def suggest_domain_experts(
        self,
        variables: list[str],
        n_experts: int = 3,
    ) -> list[str]:
        """Suggest domain expert roles relevant to `variables`."""
        ...
