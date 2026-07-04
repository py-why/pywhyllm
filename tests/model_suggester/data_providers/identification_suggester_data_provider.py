from pywhyllm.suggesters.response_models import IVFactorsResponse, MediatingFactorsResponse

# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]

# MOCK RESPONSES
test_suggest_mediator_expected_response = MediatingFactorsResponse(mediating_factors=["air pollution exposure"])
test_suggest_ivs_expected_response = IVFactorsResponse(iv_factors=["exercise habits"])

# ASSERTIONS
test_suggest_mediator_expected_results = (
    {
        ("smoking", "lung cancer"): 1,
        ("smoking", "air pollution exposure"): 1,
        ("air pollution exposure", "lung cancer"): 1,
    },
    ["air pollution exposure"],
)
test_suggest_ivs_expected_results = (
    {("smoking", "lung cancer"): 1, ("exercise habits", "smoking"): 1},
    ["exercise habits"],
)
