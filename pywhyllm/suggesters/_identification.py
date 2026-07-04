import asyncio

from ._prompts import (
    confounders_messages,
    latent_confounders_messages,
    negative_controls_messages,
)
from .response_models import (
    ConfoundingFactorsResponse,
    LatentConfoundersResponse,
    NegativeControlsResponse,
)


class IdentificationMixin:
    """
    Causal identification methods — confounders, negative controls.

    Relies on ``self.client``, ``self.context``, and ``self._api_kwargs``
    provided by ``ModelSuggester.__init__``.
    """

    # ------------------------------------------------------------------
    # Confounders
    # ------------------------------------------------------------------

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
        treatment : str
        outcome : str
        variables : list[str]
            Candidate variables to search within (ignored when ``latent=True``).
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel; results
            are unioned and deduplicated.
        latent : bool
            ``False`` (default): find confounders within ``variables``.
            ``True``: find unmeasured confounders outside ``variables``.
        """
        if not expertise_list:
            return await self._confounders_call(
                treatment, outcome, variables, expertise=None, latent=latent
            )

        results = await asyncio.gather(*[
            self._confounders_call(treatment, outcome, variables, expertise=expert, latent=latent)
            for expert in expertise_list
        ])

        seen: set[str] = set()
        merged: list[str] = []
        for result in results:
            for c in result:
                if c not in seen:
                    seen.add(c)
                    merged.append(c)
        return merged

    async def _confounders_call(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise: str | None,
        latent: bool,
    ) -> list[str]:
        if latent:
            response = await self.client.chat.completions.create(
                **self._api_kwargs,
                response_model=LatentConfoundersResponse,
                messages=latent_confounders_messages(
                    treatment, outcome, variables, self.context, expertise
                ),
            )
            return response.confounding_factors
        else:
            candidates = [v for v in variables if v not in (treatment, outcome)]
            response = await self.client.chat.completions.create(
                **self._api_kwargs,
                response_model=ConfoundingFactorsResponse,
                messages=confounders_messages(
                    treatment, outcome, candidates, self.context, expertise
                ),
            )
            return [f for f in response.confounding_factors if f in candidates]

    # ------------------------------------------------------------------
    # Negative controls
    # ------------------------------------------------------------------

    async def suggest_negative_controls(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise_list: list[str] | None = None,
    ) -> list[str]:
        """
        Suggest negative controls for the treatment → outcome relationship.

        Negative controls are variables that *should* be unaffected by
        changes in the treatment. Useful for robustness checking — if
        your model shows a treatment effect on a negative control,
        something is wrong.

        Parameters
        ----------
        treatment : str
        outcome : str
        variables : list[str]
            Candidate variables to search within.
        expertise_list : list[str] | None
            Expert roles. Multiple experts are queried in parallel.
        """
        if not expertise_list:
            return await self._negative_controls_call(
                treatment, outcome, variables, expertise=None
            )

        results = await asyncio.gather(*[
            self._negative_controls_call(treatment, outcome, variables, expertise=expert)
            for expert in expertise_list
        ])

        seen: set[str] = set()
        merged: list[str] = []
        for result in results:
            for c in result:
                if c not in seen:
                    seen.add(c)
                    merged.append(c)
        return merged

    async def _negative_controls_call(
        self,
        treatment: str,
        outcome: str,
        variables: list[str],
        expertise: str | None,
    ) -> list[str]:
        candidates = [v for v in variables if v not in (treatment, outcome)]
        response = await self.client.chat.completions.create(
            **self._api_kwargs,
            response_model=NegativeControlsResponse,
            messages=negative_controls_messages(
                treatment, outcome, candidates, self.context, expertise
            ),
        )
        return [f for f in response.negative_controls if f in candidates]
