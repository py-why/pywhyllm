EXPECTED_RESULTS_MODEL_SUGGESTER = {
    "test_var_list_expected_domain_expertises": ["<domain_expertise>Epidemiologist</domain_expertise>",
                                                 ['Epidemiologist']],
    "test_var_list_expected_domain_experts": {'Behavioral Scientist', 'Environmental Scientist', 'Epidemiologist',
                                              'Exercise Physiologist', 'Pulmonologist'},
    "test_var_list_expected_stakeholders": ['Oncologists',
                                            'Pulmonologists',
                                            'Health behavior researchers',
                                            'Environmental scientists',
                                            'Public health officials'],
    "test_var_list_expected_parents": ['exercise habits', 'air pollution exposure'],
    "test_var_list_expected_children": ['lung cancer'],
    "test_var_list_a_cause_b": ["The answer is <answer>A</answer>,", ("smoking", "lung cancer")],
    "test_var_list_b_cause_a": ["The answer is <answer>B</answer>,", ("lung cancer", "smoking")],
    "test_var_list_a_cause_b": ["The answer is <answer>C</answer>,", None]

}

TESTS_MODEL_SUGGESTER = {
    "test_var_list": ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]
}