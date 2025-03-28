# TESTS
test_vars = ["semaglutide treatment", "cardiovascular health",
             ["Age", "Sex", "HbA1c", "HDL", "LDL", "eGFR", "Prior MI",
              "Prior Stroke or TIA", "Prior Heart Failure", "Cardiovascular medication",
              "T2DM medication", "Insulin", "Morbid obesity",
              "First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause",
              "semaglutide treatment", "Semaglutide medication", "income", "musical taste"]]

# MOCK RESPONSES
test_iv_expected_response = "<iv>Insulin</iv> <iv>T2DM medication</iv> <iv>Cardiovascular medication</iv> <iv>Prior MI</iv> <iv>Prior Stroke or TIA</iv> <iv>Morbid obesity</iv>"
test_backdoor_expected_response = "<backdoor>Age</backdoor> <backdoor>Sex</backdoor> <backdoor>HbA1c</backdoor> <backdoor>HDL</backdoor> <backdoor>LDL</backdoor> <backdoor>eGFR</backdoor> <backdoor>Prior MI</backdoor> <backdoor>Prior Stroke or TIA</backdoor> <backdoor>Prior Heart Failure</backdoor> <backdoor>Cardiovascular medication</backdoor> <backdoor>T2DM medication</backdoor> <backdoor>Insulin</backdoor> <backdoor>Morbid obesity</backdoor>"
test_frontdoor_expected_response = "<frontdoor>HbA1c</frontdoor> <frontdoor>T2DM medication</frontdoor> <frontdoor>Insulin</frontdoor> <frontdoor>Cardiovascular medication</frontdoor> <frontdoor>Prior MI</frontdoor> <frontdoor>Prior Stroke or TIA</frontdoor> <frontdoor>Prior Heart Failure</frontdoor> <frontdoor>First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause</frontdoor>"

# ASSERTIONS
test_iv_expected_result = ["Insulin",
                           "T2DM medication",
                           "Cardiovascular medication",
                           "Prior MI",
                           "Prior Stroke or TIA",
                           "Morbid obesity"]
test_backdoor_expected_result = ["Age", "Sex", "HbA1c", "HDL", "LDL", "eGFR", "Prior MI", "Prior Stroke or TIA",
                                 "Prior Heart Failure", "Cardiovascular medication", "T2DM medication", "Insulin",
                                 "Morbid obesity"]
test_frontdoor_expected_result = ["HbA1c", "T2DM medication", "Insulin", "Cardiovascular medication", "Prior MI",
                                  "Prior Stroke or TIA", "Prior Heart Failure",
                                  "First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause"]
