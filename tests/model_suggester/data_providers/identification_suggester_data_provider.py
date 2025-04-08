# TESTS
test_vars = ["smoking", "lung cancer", "exercise habits", "air pollution exposure"]

# MOCK RESPONSES
test_suggest_mediator_expected_response = "<mediating_factor>air pollution exposure</mediating_factor>"
test_suggest_ivs_expected_response = "<iv_factor>exercise habits</iv_factor>"

# ASSERTIONS
test_suggest_mediator_expected_results = ({('smoking', 'lung cancer'): 1,
                                           ('smoking', 'air pollution exposure'): 1,
                                           ('air pollution exposure', 'lung cancer'): 1},
                                          ['air pollution exposure'])
test_suggest_ivs_expected_results = ({('smoking', 'lung cancer'): 1, ('exercise habits', 'smoking'): 1},
                                     ['exercise habits'])
