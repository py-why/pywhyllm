TEST_PAIRS = {
    "test_a_cause_b": ["temperature", "ice cream sales"],
    "test_a_cause_b_expected_result": ["temperature", "ice cream sales", "The answer is <answer> A </answer>."],
    "test_b_cause_a": ["cavities", "ice cream sales"],
    "test_b_cause_a_expected_result": ["ice cream sales", "cavities", "The answer is <answer> B </answer>."],
    "test_no_causality": ["ice cream sales", "shark attacks"],
    "test_no_causality_expected_result": [None, None, "The answer is <answer> C </answer>."],
}
