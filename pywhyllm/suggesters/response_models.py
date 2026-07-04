from pydantic import BaseModel, Field
from typing import Literal


# --- Graph-centric response models ---


class CausalEdge(BaseModel):
    cause: str = Field(description="The variable that causes the other")
    effect: str = Field(description="The variable that is caused")
    confidence: float = Field(
        ge=0, le=1, description="Confidence in this causal relationship (0-1)"
    )
    reasoning: str = Field(description="Step-by-step reasoning for this causal relationship")


class CausalGraphResponse(BaseModel):
    edges: list[CausalEdge] = Field(
        description="All direct causal relationships identified between the variables"
    )


# --- Expert / stakeholder discovery ---


class DomainExpertisesResponse(BaseModel):
    expertises: list[str] = Field(description="List of domain expertise areas relevant to the causal analysis")


class DomainExpertsResponse(BaseModel):
    experts: list[str] = Field(description="List of domain expert roles relevant to the causal analysis")


class StakeholdersResponse(BaseModel):
    stakeholders: list[str] = Field(description="List of stakeholders relevant to the causal analysis")


# --- Identification response models ---


class ConfoundingFactorsResponse(BaseModel):
    confounding_factors: list[str] = Field(
        description="Factors from the provided list that directly influence and cause both the treatment and outcome"
    )


class LatentConfoundersResponse(BaseModel):
    confounding_factors: list[str] = Field(
        description="Latent (unmeasured) factors that directly influence and cause both the treatment and outcome"
    )


class MediatingFactorsResponse(BaseModel):
    mediating_factors: list[str] = Field(
        description="Factors from the provided list that are on the causal chain linking treatment to outcome"
    )


class IVFactorsResponse(BaseModel):
    iv_factors: list[str] = Field(
        description=(
            "Factors from the provided list that cause the treatment but have very low "
            "likelihood of influencing the outcome"
        )
    )


class NegativeControlsResponse(BaseModel):
    negative_controls: list[str] = Field(
        description="Factors from the provided list that should be unaffected by changes in the treatment"
    )


# --- Legacy pairwise response models ---


class InfluencingFactorsResponse(BaseModel):
    influencing_factors: list[str] = Field(
        description="Factors from the provided list that directly influence or cause the target factor"
    )


class InfluencedFactorsResponse(BaseModel):
    influenced_factors: list[str] = Field(
        description="Factors from the provided list that are directly influenced or caused by the target factor"
    )


class PairwiseRelationshipResponse(BaseModel):
    thinking: str = Field(description="Step-by-step reasoning about the causal relationship")
    answer: Literal["A", "B", "C"] = Field(
        description=(
            "A if factor_a causes factor_b, B if factor_b causes factor_a, "
            "C if no causal relationship exists"
        )
    )


class SimpleConfoundersResponse(BaseModel):
    confounders: list[str] = Field(
        description="Latent confounding factors that influence the relationship between treatment and outcome"
    )
