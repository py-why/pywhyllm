from pywhyllm.suggesters.response_models import (
    ConfoundingFactorsResponse,
    DomainExpertsResponse,
    DomainExpertisesResponse,
    InfluencedFactorsResponse,
    InfluencingFactorsResponse,
    PairwiseRelationshipResponse,
    StakeholdersResponse,
)

# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]

# MOCK RESPONSES
test_domain_expertises_expected_response = DomainExpertisesResponse(expertises=["Epidemiologist"])
test_domain_experts_expected_response = DomainExpertsResponse(
    experts=[
        "Behavioral Scientist",
        "Environmental Scientist",
        "Epidemiologist",
        "Exercise Physiologist",
        "Pulmonologist",
    ]
)
test_stakeholders_expected_response = StakeholdersResponse(
    stakeholders=[
        "Oncologists",
        "Pulmonologists",
        "Health behavior researchers",
        "Environmental scientists",
        "Public health officials",
    ]
)
test_parents_expected_response = InfluencingFactorsResponse(
    influencing_factors=["exercise habits", "air pollution exposure"]
)
test_children_expected_response = InfluencedFactorsResponse(influenced_factors=["lung cancer"])
test_pairwise_a_cause_b_expected_response = PairwiseRelationshipResponse(
    thinking="Smoking is a well-known cause of lung cancer.", answer="A"
)
test_pairwise_b_cause_a_expected_response = PairwiseRelationshipResponse(
    thinking="The evidence points to lung cancer being caused by smoking, not the reverse.", answer="B"
)
test_pairwise_no_causality_expected_response = PairwiseRelationshipResponse(
    thinking="There is no direct causal relationship between these two factors.", answer="C"
)
test_request_confounders_expected_response = ConfoundingFactorsResponse(
    confounding_factors=["exercise habits", "air pollution exposure"]
)
test_suggest_relationships_parent_expected_response = [
    InfluencingFactorsResponse(influencing_factors=["air pollution exposure"]),
    InfluencingFactorsResponse(influencing_factors=["smoking", "air pollution exposure"]),
    InfluencingFactorsResponse(influencing_factors=["air pollution exposure"]),
    InfluencingFactorsResponse(influencing_factors=[]),
]
test_suggest_relationships_child_expected_response = [
    InfluencedFactorsResponse(influenced_factors=["lung cancer", "exercise habits", "air pollution exposure"]),
    InfluencedFactorsResponse(influenced_factors=[]),
    InfluencedFactorsResponse(influenced_factors=["lung cancer"]),
    InfluencedFactorsResponse(influenced_factors=["lung cancer", "exercise habits"]),
]
tests_suggest_relationships_pairwise_expected_response = [
    PairwiseRelationshipResponse(thinking="smoking causes lung cancer", answer="A"),
    PairwiseRelationshipResponse(thinking="smoking causes exercise habits", answer="A"),
    PairwiseRelationshipResponse(thinking="smoking causes air pollution", answer="A"),
    PairwiseRelationshipResponse(thinking="exercise habits caused by lung cancer", answer="B"),
    PairwiseRelationshipResponse(thinking="no causal link", answer="C"),
    PairwiseRelationshipResponse(thinking="air pollution caused by exercise habits", answer="B"),
]

# ASSERTIONS
test_domain_expertises_expected_result = ["Epidemiologist"]
test_domain_experts_expected_result = {
    "Behavioral Scientist",
    "Environmental Scientist",
    "Epidemiologist",
    "Exercise Physiologist",
    "Pulmonologist",
}
test_stakeholders_expected_results = [
    "Oncologists",
    "Pulmonologists",
    "Health behavior researchers",
    "Environmental scientists",
    "Public health officials",
]
test_parents_expected_results = ["exercise habits", "air pollution exposure"]
test_children_expected_results = ["lung cancer"]
test_a_cause_b_expected_results = ("smoking", "lung cancer")
test_b_cause_a_expected_results = ("lung cancer", "smoking")
test_no_causality_expected_results = None
test_suggest_confounders_expected_results = (
    {
        ("smoking", "lung cancer"): 1,
        ("exercise habits", "smoking"): 1,
        ("exercise habits", "lung cancer"): 1,
        ("air pollution exposure", "smoking"): 1,
        ("air pollution exposure", "lung cancer"): 1,
    },
    ["exercise habits", "air pollution exposure"],
)
test_suggest_relationships_parent_expected_results = {
    ("air pollution exposure", "exercise habits"): 1,
    ("air pollution exposure", "lung cancer"): 1,
    ("air pollution exposure", "smoking"): 1,
    ("smoking", "lung cancer"): 1,
}
test_suggest_relationships_child_expected_results = {
    ("air pollution exposure", "smoking"): 1,
    ("exercise habits", "air pollution exposure"): 1,
    ("exercise habits", "smoking"): 1,
    ("lung cancer", "air pollution exposure"): 1,
    ("lung cancer", "exercise habits"): 1,
    ("lung cancer", "smoking"): 1,
}
test_suggest_relationships_pairwise_expected_results = {
    ("air pollution exposure", "exercise habits"): 1,
    ("exercise habits", "lung cancer"): 1,
    ("smoking", "air pollution exposure"): 1,
    ("smoking", "exercise habits"): 1,
    ("smoking", "lung cancer"): 1,
}
test_suggest_relationships_confounders_expected_results = (
    {
        ("smoking", "lung cancer"): 1,
        ("exercise habits", "smoking"): 1,
        ("exercise habits", "lung cancer"): 1,
        ("air pollution exposure", "smoking"): 1,
        ("air pollution exposure", "lung cancer"): 1,
    },
    ["exercise habits", "air pollution exposure"],
)
