"""
Prompt builders for ModelSuggester.

Each function returns a ``messages`` list ready to pass directly to
``client.chat.completions.create``.  All prompt text lives here —
the mixin methods contain no inline strings.

Convention
----------
Every builder takes only the parameters it needs and returns::

    [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
"""


# ---------------------------------------------------------------------------
# Discovery — graph
# ---------------------------------------------------------------------------

def graph_messages(
    variables: list[str],
    context: str,
    expertise: str | None,
) -> list[dict]:
    system = (
        f"You are an expert in {expertise} studying {context}. "
        f"You are building a causal model that describes the causal mechanisms of this system."
        if expertise
        else f"You are a helpful assistant for causal reasoning about {context}."
    )
    user = (
        f"Given these variables: {variables}\n\n"
        f"Identify all direct causal relationships between them. "
        f"Think step by step. Only include relationships with a high likelihood "
        f"of being directly causally true. "
        f"Do not include indirect relationships or feedback loops."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------------------------------------------------------------------------
# Discovery — experts / stakeholders
# ---------------------------------------------------------------------------

def domain_experts_messages(variables: list[str], n_experts: int) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant for recommending domain experts.",
        },
        {
            "role": "user",
            "content": (
                f"What domain experts have the knowledge and experience needed to identify "
                f"causal relationships between: {variables}? "
                f"Think step by step and recommend {n_experts} domain experts."
            ),
        },
    ]


def domain_expertises_messages(variables: list[str], n_experts: int) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant for recommending domain expertises.",
        },
        {
            "role": "user",
            "content": (
                f"What domain expertises are needed to identify causal relationships "
                f"between: {variables}? "
                f"Think step by step and recommend {n_experts} expertises."
            ),
        },
    ]


def stakeholders_messages(variables: list[str], n_stakeholders: int) -> list[dict]:
    return [
        {
            "role": "system",
            "content": "You are a helpful assistant for recommending stakeholders.",
        },
        {
            "role": "user",
            "content": (
                f"What stakeholders have knowledge and experience relevant to "
                f"causal relationships between: {variables}? "
                f"Think step by step and recommend {n_stakeholders} stakeholders."
            ),
        },
    ]


# ---------------------------------------------------------------------------
# Identification — confounders
# ---------------------------------------------------------------------------

def confounders_messages(
    treatment: str,
    outcome: str,
    candidates: list[str],
    context: str,
    expertise: str | None,
) -> list[dict]:
    """Observed confounders — searched within a known candidate list."""
    system = (
        f"You are an expert in {expertise} studying {context}."
        if expertise
        else "You are a helpful assistant for causal reasoning."
    )
    user = (
        f"From these factors: {candidates}\n\n"
        f"Which, if any, directly cause both {treatment} and {outcome}? "
        f"Think step by step. Only include factors with a high likelihood of "
        f"confounding the relationship between {treatment} and {outcome}."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def latent_confounders_messages(
    treatment: str,
    outcome: str,
    variables: list[str],
    context: str,
    expertise: str | None,
) -> list[dict]:
    """Latent (unmeasured) confounders — outside the known variable list."""
    system = (
        f"You are an expert in {expertise} studying {context}."
        if expertise
        else "You are a helpful assistant for causal reasoning."
    )
    user = (
        f"What latent (unmeasured) confounding factors might influence the relationship "
        f"between {treatment} and {outcome}? "
        f"We have already considered the following factors: {variables}. "
        f"Do not repeat them. List only confounding factors not already in that list."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------------------------------------------------------------------------
# Identification — negative controls
# ---------------------------------------------------------------------------

def negative_controls_messages(
    treatment: str,
    outcome: str,
    candidates: list[str],
    context: str,
    expertise: str | None,
) -> list[dict]:
    system = (
        f"You are an expert in {expertise} studying {context}."
        if expertise
        else "You are a helpful assistant for causal reasoning."
    )
    user = (
        f"From these factors: {candidates}\n\n"
        f"Which, if any, should see zero treatment effect when changing {treatment}? "
        f"Which factors should be completely unaffected by changes in {treatment} "
        f"and are unrelated to the causal mechanisms that affect {outcome}? "
        f"Think step by step. Only include factors you are confident are negative controls."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------------------------------------------------------------------------
# Validation — critique
# ---------------------------------------------------------------------------

def critique_messages(
    variables: list[str],
    edge_block: str,
    context: str,
    expertise: str | None,
) -> list[dict]:
    system = (
        f"You are an expert in {expertise} studying {context}. "
        f"You are reviewing a proposed causal model for correctness."
        if expertise
        else f"You are a helpful assistant reviewing a proposed causal model about {context}."
    )
    user = (
        f"A causal model has been proposed with these variables: {variables}\n\n"
        f"The proposed causal edges are:\n{edge_block}\n\n"
        f"Review each edge. Think step by step about whether each represents "
        f"a valid, direct causal relationship. "
        f"Return only the edges you believe are correct. "
        f"Also add any direct causal edges you believe are missing. "
        f"Do not include indirect relationships or feedback loops."
    )
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]
