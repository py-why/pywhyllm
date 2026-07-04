from pywhyllm.suggesters.response_models import (
    InfluencedFactorsResponse,
    InfluencingFactorsResponse,
    LatentConfoundersResponse,
    NegativeControlsResponse,
    PairwiseRelationshipResponse,
)

# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]
domain_expertises = ["Epidemiology"]

# MOCK RESPONSES
test_latent_confounders_expected_response = LatentConfoundersResponse(
    confounding_factors=["socio-economic status", "mental health"]
)
test_negative_controls_expected_response = NegativeControlsResponse(negative_controls=["exercise habits"])
test_parent_critique_expected_response = InfluencingFactorsResponse(influencing_factors=[])
test_children_critique_expected_response = InfluencedFactorsResponse(influenced_factors=["lung cancer"])
test_pairwise_critique_expected_response = PairwiseRelationshipResponse(
    thinking="Smoking is a well-established cause of lung cancer.", answer="A"
)
test_critique_graph_parent_expected_response = [
    InfluencingFactorsResponse(influencing_factors=[]),
    InfluencingFactorsResponse(influencing_factors=["smoking", "air pollution exposure"]),
    InfluencingFactorsResponse(influencing_factors=["air pollution exposure"]),
    InfluencingFactorsResponse(influencing_factors=[]),
]
test_critique_graph_children_expected_response = [
    InfluencedFactorsResponse(influenced_factors=["lung cancer"]),
    InfluencedFactorsResponse(influenced_factors=["exercise habits"]),
    InfluencedFactorsResponse(influenced_factors=["lung cancer"]),
    InfluencedFactorsResponse(influenced_factors=["lung cancer", "exercise habits"]),
]
test_critique_graph_pairwise_expected_response = [
    PairwiseRelationshipResponse(thinking="smoking causes lung cancer", answer="A"),
    PairwiseRelationshipResponse(thinking="smoking causes exercise habits", answer="A"),
    PairwiseRelationshipResponse(thinking="no causal link", answer="C"),
    PairwiseRelationshipResponse(thinking="air pollution caused by lung cancer", answer="B"),
    PairwiseRelationshipResponse(thinking="air pollution affects exercise habits", answer="B"),
    PairwiseRelationshipResponse(thinking="exercise habits affected by air pollution", answer="B"),
]

# ASSERTIONS
test_suggest_latent_confounders_expected_results = (
    {"socio-economic status": 1, "mental health": 1},
    [
        {"socio-economic status": 1, "mental health": 1},
        ["socio-economic status", "mental health"],
    ],
)
test_request_latent_confounders_expected_results = (
    {"socio-economic status": 1, "mental health": 1},
    ["socio-economic status", "mental health"],
)
test_suggest_negative_controls_expected_results = (
    {"exercise habits": 1},
    [{"exercise habits": 1}, ["exercise habits"]],
)
test_request_negative_controls_expected_results = ({"exercise habits": 1}, ["exercise habits"])
test_parent_critique_expected_results = []
test_children_critique_expected_results = ["lung cancer"]
test_pairwise_critique_expected_results = ("smoking", "lung cancer")
test_critique_graph_parent_expected_results = (
    {
        ("air pollution exposure", "exercise habits"): 1,
        ("air pollution exposure", "lung cancer"): 1,
        ("air pollution exposure", "smoking"): 1,
        ("smoking", "lung cancer"): 1,
    },
    {
        ("air pollution exposure", "exercise habits"): 1,
        ("air pollution exposure", "lung cancer"): 1,
        ("smoking", "lung cancer"): 1,
    },
)
test_critique_graph_children_expected_results = (
    {
        ("air pollution exposure", "smoking"): 1,
        ("exercise habits", "air pollution exposure"): 1,
        ("exercise habits", "smoking"): 1,
        ("lung cancer", "air pollution exposure"): 1,
        ("lung cancer", "exercise habits"): 1,
        ("lung cancer", "smoking"): 1,
    },
    {
        ("exercise habits", "air pollution exposure"): 1,
        ("exercise habits", "lung cancer"): 1,
        ("lung cancer", "air pollution exposure"): 1,
        ("lung cancer", "exercise habits"): 1,
        ("lung cancer", "smoking"): 1,
    },
)
test_critique_graph_pairwise_expected_results = (
    {
        ("air pollution exposure", "exercise habits"): 1,
        ("exercise habits", "lung cancer"): 1,
        ("smoking", "air pollution exposure"): 1,
        ("smoking", "exercise habits"): 1,
        ("smoking", "lung cancer"): 1,
    },
    {
        ("smoking", "lung cancer"): 1,
        ("smoking", "exercise habits"): 1,
        ("exercise habits", "lung cancer"): 1,
        ("air pollution exposure", "lung cancer"): 1,
        ("air pollution exposure", "exercise habits"): 1,
    },
)
