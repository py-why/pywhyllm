# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]

# MOCK RESPONSES
test_domain_expertises_expected_response = "<domain_expertise>Epidemiologist</domain_expertise>"
test_domain_experts_expected_response = "<domain_expert>Behavioral Scientist</domain_expert> <domain_expert>Environmental Scientist</domain_expert> <domain_expert>Epidemiologist</domain_expert> <domain_expert>Exercise Physiologist</domain_expert> <domain_expert>Pulmonologist</domain_expert>"
test_stakeholders_expected_response = "<stakeholder>Oncologists</stakeholder> <stakeholder>Pulmonologists</stakeholder> <stakeholder>Health behavior researchers</stakeholder> <stakeholder>Environmental scientists</stakeholder> <stakeholder>Public health officials</stakeholder>"
test_parents_expected_response = "<influencing_factor>exercise habits</influencing_factor> <influencing_factor>air pollution exposure</influencing_factor>"
test_children_expected_response = "<influenced_factor>lung cancer</influenced_factor>"
test_pairwise_a_cause_b_expected_response = "The answer is <answer>A</answer>"
test_pairwise_b_cause_a_expected_response = "The answer is <answer>B</answer>"
test_pairwise_no_causality_expected_response = "The answer is <answer>C</answer>"
test_request_confounders_expected_response = "<confounding_factor>exercise habits</confounding_factor> <confounding_factor>air pollution exposure</confounding_factor>"
test_suggest_relationships_parent_expected_response = [
    "<influencing_factor>air pollution exposure</influencing_factor>",
    "<influencing_factor>smoking</influencing_factor> <influencing_factor>air pollution exposure</influencing_factor>",
    "<influencing_factor>air pollution exposure</influencing_factor>",
    "None"]
test_suggest_relationships_child_expected_response = [
    "<influenced_factor>lung cancer</influenced_factor><influenced_factor>exercise habits</influenced_factor><influenced_factor>air pollution exposure</influenced_factor>",
    "None",
    "<influenced_factor>lung cancer</influenced_factor>",
    "<influenced_factor>lung cancer</influenced_factor><influenced_factor>exercise habits</influenced_factor>"
]
tests_suggest_relationships_pairwise_expected_response = ["<answer>A</answer>", "<answer>A</answer>",
                                                          "<answer>A</answer>", "<answer>B</answer>",
                                                          "<answer>C</answer>", "<answer>B</answer>",
                                                          "<answer>C</answer>", "<answer>B</answer>",
                                                          "<answer>B</answer>", "<answer>B</answer>",
                                                          "<answer>A</answer>", "<answer>C</answer>"]

# ASSERTIONS
test_domain_expertises_expected_result = ['Epidemiologist']
test_domain_experts_expected_result = {'Behavioral Scientist', 'Environmental Scientist', 'Epidemiologist',
                                       'Exercise Physiologist', 'Pulmonologist'}
test_stakeholders_expected_results = ['Oncologists',
                                      'Pulmonologists',
                                      'Health behavior researchers',
                                      'Environmental scientists',
                                      'Public health officials']
test_parents_expected_results = ['exercise habits', 'air pollution exposure']
test_children_expected_results = ['lung cancer']
test_a_cause_b_expected_results = ("smoking", "lung cancer")
test_b_cause_a_expected_results = ("lung cancer", "smoking")
test_no_causality_expected_results = None
test_suggest_confounders_expected_results = ({('smoking', 'lung cancer'): 1,
                                              ('exercise habits', 'smoking'): 1,
                                              ('exercise habits', 'lung cancer'): 1,
                                              ('air pollution exposure', 'smoking'): 1,
                                              ('air pollution exposure', 'lung cancer'): 1},
                                             ['exercise habits', 'air pollution exposure'])
test_suggest_relationships_parent_expected_results = {('air pollution exposure', 'exercise habits'): 1,
                                                      ('air pollution exposure', 'lung cancer'): 1,
                                                      ('air pollution exposure', 'smoking'): 1,
                                                      ('smoking', 'lung cancer'): 1}
test_suggest_relationships_child_expected_results = {('air pollution exposure', 'smoking'): 1,
                                                     ('exercise habits', 'air pollution exposure'): 1,
                                                     ('exercise habits', 'smoking'): 1,
                                                     ('lung cancer', 'air pollution exposure'): 1,
                                                     ('lung cancer', 'exercise habits'): 1,
                                                     ('lung cancer', 'smoking'): 1}
test_suggest_relationships_pairwise_expected_results = {('air pollution exposure', 'exercise habits'): 1,
                                                        ('exercise habits', 'lung cancer'): 1,
                                                        ('smoking', 'air pollution exposure'): 1,
                                                        ('smoking', 'exercise habits'): 1,
                                                        ('smoking', 'lung cancer'): 1}
test_suggest_relationships_confounders_expected_results = ({('smoking', 'lung cancer'): 1,
                                                            ('exercise habits', 'smoking'): 1,
                                                            ('exercise habits', 'lung cancer'): 1,
                                                            ('air pollution exposure', 'smoking'): 1,
                                                            ('air pollution exposure', 'lung cancer'): 1},
                                                           ['exercise habits', 'air pollution exposure'])
