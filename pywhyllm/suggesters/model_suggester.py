import instructor
from openai import AsyncOpenAI

from ._discovery import DiscoveryMixin
from ._identification import IdentificationMixin
from ._validation import ValidationMixin


class ModelSuggester(DiscoveryMixin, IdentificationMixin, ValidationMixin):
    """
    LLM-backed causal model suggester.

    Combines discovery, identification, and validation capabilities
    into a single interface. Build a causal graph, identify confounders
    and negative controls, and critique the graph — all with async
    parallelisation across domain experts.

    Parameters
    ----------
    client :
        An async instructor-patched client, e.g.
        ``instructor.from_openai(AsyncOpenAI())``.
        Supports any provider instructor wraps (OpenAI, Anthropic, Gemini, etc.).
    model : str
        Model name passed to the client, e.g. ``"gpt-4o"``.
    context : str
        Short description of the domain, e.g. ``"cardiovascular health"``.
        Injected into every system prompt.

    Examples
    --------
    Full workflow::

        suggester = ModelSuggester(
            client=instructor.from_openai(AsyncOpenAI()),
            model="gpt-4o",
            context="cardiovascular health",
        )

        # Discovery
        experts = await suggester.suggest_domain_experts(variables)
        graph   = await suggester.suggest_graph(variables, expertise_list=experts)

        # Local queries — zero LLM calls
        graph.parents_of("lung_cancer")
        graph.mediators_of("smoking", "lung_cancer")

        # Identification
        confounders = await suggester.suggest_confounders("smoking", "lung_cancer", variables)
        negatives   = await suggester.suggest_negative_controls("smoking", "lung_cancer", variables)

        # Validation
        critique = await suggester.critique_graph(graph, variables, expertise_list=experts)
    """

    DEFAULT_CONTEXT: str = "causal mechanisms"

    def __init__(
        self,
        client=None,
        model: str = "gpt-4o",
        context: str = DEFAULT_CONTEXT,
        temperature: float | None = None,
    ):
        self.model = model
        self.context = context
        self.temperature = temperature
        self.client = client if client is not None else instructor.from_openai(AsyncOpenAI())

    @property
    def _api_kwargs(self) -> dict:
        """Base kwargs passed to every client.chat.completions.create call."""
        kwargs = {"model": self.model}
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        return kwargs
