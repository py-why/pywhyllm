EXPECTED_RESULTS_SIMPLE_MODEL_SUGGESTER = {
    "test_a_cause_b_expected_result": ["temperature", "ice cream sales", "The answer is <answer>A</answer>."],
    "test_a_cause_b_expected_relationships": {("temperature", "ice cream sales"): "The answer is <answer>A</answer>."},
    "test_b_cause_a_expected_result": ["ice cream sales", "temperature", "The answer is <answer>B</answer>."],
    "test_b_cause_a_expected_relationships": {("ice cream sales", "temperature"): "The answer is <answer>B</answer>."},
    "test_no_causality_expected_result": [None, None, "The answer is <answer>C</answer>."],
    "test_no_causality_expected_relationships": {
        ("temperature", "ice cream sales"): "The answer is <answer>C</answer>."},
    "test_three_var_list_expected_pairwise_descriptions": ["The answer is <answer>A</answer>.",
                                                           "The answer is <answer>C</answer>.",
                                                           "The answer is <answer>C</answer>."],
    "test_three_var_list_expected_relationships": {
        ('temperature', 'ice cream sales'): "The answer is <answer>A</answer>."},
    "test_four_var_list_expected_pairwise_descriptions": ["The answer is <answer>A</answer>.",
                                                          "The answer is <answer>C</answer>.",
                                                          "The answer is <answer>A</answer>.",
                                                          "The answer is <answer>C</answer>.",
                                                          "The answer is <answer>B</answer>.",
                                                          "The answer is <answer>B</answer>."],
    "test_four_var_list_expected_relationships": {('smoking', 'lung cancer'): "The answer is <answer>A</answer>.",
                                                  ('smoking',
                                                   'air pollution exposure'): "The answer is <answer>A</answer>.",
                                                  ('air pollution exposure',
                                                   'lung cancer'): "The answer is <answer>B</answer>.",
                                                  ('air pollution exposure',
                                                   'exercise habits'): "The answer is <answer>B</answer>."
                                                  },
    "test_confounders_expected_result": [
        "<conf>Beach attendance</conf> <conf>Water temperature</conf> <conf>Availability of ice cream</conf> <conf>Shark population</conf> <conf>Public holidays</conf> <conf>Leisure time</conf> <conf>Tourist season</conf> <conf>Swimming habits</conf>",
        ['Beach attendance', 'Water temperature',
         'Availability of ice cream', 'Shark population', 'Public holidays',
         'Leisure time', 'Tourist season', 'Swimming habits']]
}

EXPECTED_RESULTS_SIMPLE_IDENTIFICATION_SUGGESTER = {
    "test_var_list_expected_ivs": [
        "<iv>Insulin</iv> <iv>T2DM medication</iv> <iv>Cardiovascular medication</iv> <iv>Prior MI</iv> <iv>Prior Stroke or TIA</iv> <iv>Morbid obesity</iv>",
        ["Insulin",
         "T2DM medication",
         "Cardiovascular medication",
         "Prior MI",
         "Prior Stroke or TIA",
         "Morbid obesity"]],
    "test_var_list_expected_backdoors": [
        "<backdoor>Age</backdoor> <backdoor>Sex</backdoor> <backdoor>HbA1c</backdoor> <backdoor>HDL</backdoor> <backdoor>LDL</backdoor> <backdoor>eGFR</backdoor> <backdoor>Prior MI</backdoor> <backdoor>Prior Stroke or TIA</backdoor> <backdoor>Prior Heart Failure</backdoor> <backdoor>Cardiovascular medication</backdoor> <backdoor>T2DM medication</backdoor> <backdoor>Insulin</backdoor> <backdoor>Morbid obesity</backdoor>",
        ["Age", "Sex", "HbA1c", "HDL", "LDL", "eGFR", "Prior MI", "Prior Stroke or TIA",
         "Prior Heart Failure", "Cardiovascular medication", "T2DM medication", "Insulin", "Morbid obesity"]],
    "test_var_list_expected_frontdoors": [
        "<frontdoor>HbA1c</frontdoor> <frontdoor>T2DM medication</frontdoor> <frontdoor>Insulin</frontdoor> <frontdoor>Cardiovascular medication</frontdoor> <frontdoor>Prior MI</frontdoor> <frontdoor>Prior Stroke or TIA</frontdoor> <frontdoor>Prior Heart Failure</frontdoor> <frontdoor>First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause</frontdoor>",
        ["HbA1c", "T2DM medication", "Insulin", "Cardiovascular medication", "Prior MI",
          "Prior Stroke or TIA", "Prior Heart Failure",
          "First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause"]]
}
