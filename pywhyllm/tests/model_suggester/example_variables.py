TEST_PAIRS = {
    "test_a_cause_b": ["temperature", "ice cream sales"],
    "test_a_cause_b_expected_result": ["temperature", "ice cream sales", "The answer is <answer> A </answer>."],
    "test_b_cause_a": ["temperature", "ice cream sales"],
    "test_b_cause_a_expected_result": ["ice cream sales", "temperature", "The answer is <answer> B </answer>."],
    "test_no_causality": ["temperature", "ice cream sales"],
    "test_no_causality_expected_result": [None, None, "The answer is <answer> C </answer>."],
}

TEST_VARIABLE_LISTS = {
    "list1": ["temperature", "ice cream sales", "cavities"],
    "list1_expected_pairwise_description": ["The answer is <answer> A </answer>.",
                                            "The answer is <answer> C </answer>.",
                                            "The answer is <answer> C </answer>."],
    "list1_expected_result": {('temperature', 'ice cream sales'): "The answer is <answer> A </answer>."},
    "list1_expected_confounders_result": ['Beach attendance', 'Water temperature',
                                          'Availability of ice cream', 'Shark population', 'Public holidays',
                                          'Leisure time', 'Tourist season', 'Swimming habits'],
    "list2": ["smoking", "lung cancer", "exercise habits", "air pollution exposure"],
    "list2_expected_pairwise_description": ["The answer is <answer> A </answer>.",
                                            "The answer is <answer> C </answer>.",
                                            "The answer is <answer> A </answer>.",
                                            "The answer is <answer> C </answer>.",
                                            "The answer is <answer> B </answer>.",
                                            "The answer is <answer> B </answer>."],
    "list2_expected_result": {('smoking', 'lung cancer'): "The answer is <answer> A </answer>.",
                              ('smoking', 'air pollution exposure'): "The answer is <answer> A </answer>.",
                              ('air pollution exposure', 'lung cancer'): "The answer is <answer> B </answer>.",
                              ('air pollution exposure', 'exercise habits'): "The answer is <answer> B </answer>."
                              },
    "list3": ["cigarette taxes", "rain", "car sales", "property taxes", "heart attacks"],
    "list3_expected_ivs_result": ["cigarette taxes"],
    "list4": ["Age", "Sex", "HbA1c", "HDL", "LDL", "eGFR", "Prior MI",
              "Prior Stroke or TIA", "Prior Heart Failure", "Cardiovascular medication",
              "T2DM medication", "Insulin", "Morbid obesity",
              "First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause",
              "semaglutide treatment", "Semaglutide medication", "income", "musical taste"],
    "list4_expected_backdoor_result": ["'Age'", "'Sex'", "'HbA1c'", "'HDL'", "'LDL'", "'eGFR'", "'Prior MI'",
                                       "'Prior Stroke or TIA'", "'Prior Heart Failure'",
                                       "'Cardiovascular medication'", "'T2DM medication'", "'Insulin'",
                                       "'Morbid obesity'"],
    "list4_expected_frontdoor_result": ["'HbA1c'", "'T2DM medication'", "'Insulin'", "'Cardiovascular medication'",
                                        "'Prior MI'", "'Prior Stroke or TIA'", "'Prior Heart Failure'",
                                        "'First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause'"]

}

# TEST_PAIRS = {
#
#     #imaginary graph with 3 nodes, "temperature", "ice cream sales" and "shark attacks"
#     "test_a_cause_b": ["temperature", "ice cream sales"],
#     "test_a_cause_b_expected_result": ["temperature", "ice cream sales", "The answer is <answer> A </answer>."],
#     "test_b_cause_a": ["temperature", "ice cream sales"],
#     "test_b_cause_a_expected_result": ["ice cream sales", "temperature", "The answer is <answer> B </answer>."],
#     "test_no_causality": ["temperature", "ice cream sales"],
#     "test_no_causality_expected_result": [None, None, "The answer is <answer> C </answer>."],
#
#     "test_a_cause_c": ["temperature", "shark attacks"],
#     "test_a_cause_c_expected_result": ["temperature", "shark attacks", "The answer is <answer> A </answer>."],
#     "test_c_cause_a": ["temperature", "shark attacks"],
#     "test_c_cause_a_expected_result": ["shark attacks", "temperature", "The answer is <answer> B </answer>."],
#     "test_no_causality": ["temperature", "shark attacks"],
#     "test_no_causality_expected_result": [None, None, "The answer is <answer> C </answer>."],
#
#     "test_b_cause_c": ["ice cream sales", "shark attacks"],
#     "test_b_cause_c_expected_result": ["ice cream sales", "shark attacks", "The answer is <answer> A </answer>."],
#     "test_c_cause_b": ["ice cream sales", "shark attacks"],
#     "test_c_cause_b_expected_result": ["shark attacks", "ice cream sales", "The answer is <answer> B </answer>."],
#     "test_no_causality": ["ice cream sales", "shark attacks"],
#     "test_no_causality_expected_result": [None, None, "The answer is <answer> C </answer>."],
#
#
# }
