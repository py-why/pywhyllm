# TESTS
test_a_cause_b = ["temperature", "ice cream sales"]
test_b_cause_a = ["temperature", "ice cream sales"]
test_no_causality = ["temperature", "ice cream sales"]
test_three_var = ["temperature", "ice cream sales", "cavities"]
test_four_var = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]
test_confounders = ["season", "shark attacks", "temperature", "ice cream sales", "cavities"]

# MOCK RESPONSES
test_a_cause_b_response = "The answer is <answer>A</answer>."
test_b_cause_a_response = "The answer is <answer>B</answer>."
test_no_causality_response = "The answer is <answer>C</answer>."
test_three_var_response = ["The answer is <answer>A</answer>.", "The answer is <answer>C</answer>.",
                                "The answer is <answer>C</answer>."]
test_four_var_response = ["The answer is <answer>A</answer>.",
                               "The answer is <answer>C</answer>.",
                               "The answer is <answer>A</answer>.",
                               "The answer is <answer>C</answer>.",
                               "The answer is <answer>B</answer>.",
                               "The answer is <answer>B</answer>."]
test_confounders_response = "<conf>Beach attendance</conf> <conf>Water temperature</conf> <conf>Availability of ice cream</conf> <conf>Shark population</conf> <conf>Public holidays</conf> <conf>Leisure time</conf> <conf>Tourist season</conf> <conf>Swimming habits</conf>"

# ASSERTIONS
test_a_cause_b_expected_result = ["temperature", "ice cream sales", "The answer is <answer>A</answer>."]
test_a_cause_b_expected_relationships = {("temperature", "ice cream sales"): "The answer is <answer>A</answer>."}
test_b_cause_a_expected_result = ["ice cream sales", "temperature", "The answer is <answer>B</answer>."]
test_b_cause_a_expected_relationships = {("ice cream sales", "temperature"): "The answer is <answer>B</answer>."}
test_no_causality_expected_result = [None, None, "The answer is <answer>C</answer>."]
test_no_causality_expected_relationships = {
    ("temperature", "ice cream sales"): "The answer is <answer>C</answer>."}
test_three_var_expected_relationships = {
    ('temperature', 'ice cream sales'): "The answer is <answer>A</answer>."}
test_four_var_expected_relationships = {('smoking', 'lung cancer'): "The answer is <answer>A</answer>.",
                                        ('smoking',
                                              'air pollution exposure'): "The answer is <answer>A</answer>.",
                                        ('air pollution exposure',
                                              'lung cancer'): "The answer is <answer>B</answer>.",
                                        ('air pollution exposure',
                                              'exercise habits'): "The answer is <answer>B</answer>."
                                        }
test_confounders_expected_result = ['Beach attendance', 'Water temperature',
                                    'Availability of ice cream', 'Shark population', 'Public holidays',
                                    'Leisure time', 'Tourist season', 'Swimming habits']
