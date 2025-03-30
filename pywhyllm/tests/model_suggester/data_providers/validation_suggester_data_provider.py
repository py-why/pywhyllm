# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]
domain_expertises = ['Epidemiology']

# MOCK RESPONSES
test_latent_confounders_expected_response = "<confounding_factor>socio-economic status</confounding_factor> <confounding_factor>mental health</confounding_factor>"
test_negative_controls_expected_response = "<negative_control>exercise habits</negative_control>"
test_parent_critique_expected_response = "None"
test_children_critique_expected_response = "<influenced_factor>lung cancer</influenced_factor>"
test_pairwise_critique_expected_response = "The answer is <answer>A</answer>"
test_critique_graph_parent_expected_response = ["None",
                                                "<influencing_factor>smoking</influencing_factor> <influencing_factor>air pollution exposure</influencing_factor>",
                                                "<influencing_factor>air pollution exposure</influencing_factor>",
                                                "None"]
test_critique_graph_children_expected_response = ["<influenced_factor>lung cancer</influenced_factor>",
                                                  "<influenced_factor>exercise habits</influenced_factor>",
                                                  "<influenced_factor>lung cancer</influenced_factor>",
                                                  "<influenced_factor>lung cancer</influenced_factor> <influenced_factor>exercise habits</influenced_factor>"]
test_critique_graph_pairwise_expected_response = ["<answer>A</answer>", "<answer>A</answer>", "<answer>C</answer>",
                                                  "<answer>B</answer>", "<answer>B</answer>", "<answer>B</answer>"]

# ASSERTIONS
test_latent_confounders_expected_results = ({'mental health': 1, 'socio-economic status': 1},
                                            ['socio-economic status', 'mental health'])
test_negative_controls_expected_results = ({'exercise habits': 1}, ['exercise habits'])
test_parent_critique_expected_results = []
test_children_critique_expected_results = ['lung cancer']
test_pairwise_critique_expected_results = ('smoking', 'lung cancer')
test_critique_graph_parent_expected_results = ({('air pollution exposure', 'exercise habits'): 1,
                                                ('air pollution exposure', 'lung cancer'): 1,
                                                ('air pollution exposure', 'smoking'): 1,
                                                ('smoking', 'lung cancer'): 1},
                                               {('air pollution exposure', 'exercise habits'): 1,
                                                ('air pollution exposure', 'lung cancer'): 1,
                                                ('smoking', 'lung cancer'): 1})
test_critique_graph_children_expected_results = ({('air pollution exposure', 'smoking'): 1,
                                                  ('exercise habits', 'air pollution exposure'): 1,
                                                  ('exercise habits', 'smoking'): 1,
                                                  ('lung cancer', 'air pollution exposure'): 1,
                                                  ('lung cancer', 'exercise habits'): 1,
                                                  ('lung cancer', 'smoking'): 1},
                                                 {('exercise habits', 'air pollution exposure'): 1,
                                                  ('exercise habits', 'lung cancer'): 1,
                                                  ('lung cancer', 'air pollution exposure'): 1,
                                                  ('lung cancer', 'exercise habits'): 1,
                                                  ('lung cancer', 'smoking'): 1})
test_critique_graph_pairwise_expected_results = ({('air pollution exposure', 'exercise habits'): 1,
                                                  ('exercise habits', 'lung cancer'): 1,
                                                  ('smoking', 'air pollution exposure'): 1,
                                                  ('smoking', 'exercise habits'): 1,
                                                  ('smoking', 'lung cancer'): 1},
                                                 {('smoking', 'lung cancer'): 1,
                                                  ('smoking', 'exercise habits'): 1,
                                                  ('exercise habits', 'lung cancer'): 1,
                                                  ('air pollution exposure', 'lung cancer'): 1,
                                                  ('air pollution exposure', 'exercise habits'): 1})
