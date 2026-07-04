from pywhyllm.suggesters.response_models import PairwiseRelationshipResponse, SimpleConfoundersResponse

# TESTS
test_a_cause_b = ["temperature", "ice cream sales"]
test_b_cause_a = ["temperature", "ice cream sales"]
test_no_causality = ["temperature", "ice cream sales"]
test_three_var = ["temperature", "ice cream sales", "cavities"]
test_four_var = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]
test_confounders = ["season", "shark attacks", "temperature", "ice cream sales", "cavities"]

# MOCK RESPONSES
test_a_cause_b_response = PairwiseRelationshipResponse(
    thinking="Higher temperatures lead people to buy more ice cream.", answer="A"
)
test_b_cause_a_response = PairwiseRelationshipResponse(
    thinking="Ice cream sales are driven by temperature, not the other way around.", answer="B"
)
test_no_causality_response = PairwiseRelationshipResponse(
    thinking="Temperature and ice cream sales are correlated but neither causes the other directly.", answer="C"
)
test_three_var_response = [
    PairwiseRelationshipResponse(thinking="Temperature causes ice cream sales.", answer="A"),
    PairwiseRelationshipResponse(thinking="No direct causal link between temperature and cavities.", answer="C"),
    PairwiseRelationshipResponse(thinking="No direct causal link between ice cream sales and cavities.", answer="C"),
]
test_four_var_response = [
    PairwiseRelationshipResponse(thinking="Smoking causes lung cancer.", answer="A"),
    PairwiseRelationshipResponse(thinking="No direct link between smoking and exercise habits.", answer="C"),
    PairwiseRelationshipResponse(thinking="Smoking causes air pollution exposure indirectly.", answer="A"),
    PairwiseRelationshipResponse(thinking="No direct link between lung cancer and exercise habits.", answer="C"),
    PairwiseRelationshipResponse(thinking="Air pollution causes lung cancer.", answer="B"),
    PairwiseRelationshipResponse(thinking="Air pollution affects exercise habits.", answer="B"),
]
test_confounders_response = SimpleConfoundersResponse(
    confounders=[
        "Beach attendance",
        "Water temperature",
        "Availability of ice cream",
        "Shark population",
        "Public holidays",
        "Leisure time",
        "Tourist season",
        "Swimming habits",
    ]
)

# ASSERTIONS
_a_thinking = "Higher temperatures lead people to buy more ice cream."
_b_thinking = "Ice cream sales are driven by temperature, not the other way around."
_c_thinking = "Temperature and ice cream sales are correlated but neither causes the other directly."

test_a_cause_b_expected_result = ["temperature", "ice cream sales", _a_thinking]
test_a_cause_b_expected_relationships = {("temperature", "ice cream sales"): _a_thinking}
test_b_cause_a_expected_result = ["ice cream sales", "temperature", _b_thinking]
test_b_cause_a_expected_relationships = {("ice cream sales", "temperature"): _b_thinking}
test_no_causality_expected_result = [None, None, _c_thinking]
test_no_causality_expected_relationships = {}
test_three_var_expected_relationships = {
    ("temperature", "ice cream sales"): "Temperature causes ice cream sales."
}
test_four_var_expected_relationships = {
    ("smoking", "lung cancer"): "Smoking causes lung cancer.",
    ("smoking", "air pollution exposure"): "Smoking causes air pollution exposure indirectly.",
    ("air pollution exposure", "lung cancer"): "Air pollution causes lung cancer.",
    ("air pollution exposure", "exercise habits"): "Air pollution affects exercise habits.",
}
test_confounders_expected_result = [
    "Beach attendance",
    "Water temperature",
    "Availability of ice cream",
    "Shark population",
    "Public holidays",
    "Leisure time",
    "Tourist season",
    "Swimming habits",
]
