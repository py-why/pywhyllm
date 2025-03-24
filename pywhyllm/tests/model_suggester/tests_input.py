TESTS_SIMPLE_MODEL_SUGGESTER = {
    "test_a_cause_b": ["temperature", "ice cream sales"],
    "test_b_cause_a": ["temperature", "ice cream sales"],
    "test_no_causality": ["temperature", "ice cream sales"],
    "test_three_var_list": ["temperature", "ice cream sales", "cavities"],
    "test_four_var_list": ["smoking", "lung cancer", "exercise habits", "air pollution exposure"],
    "test_confounders": ["season", "shark attacks", "temperature", "ice cream sales", "cavities"],
}

TESTS_SIMPLE_IDENTIFICATION_SUGGESTER = {
    "test_var_list": ["semaglutide treatment", "cardiovascular health",
                      ["Age", "Sex", "HbA1c", "HDL", "LDL", "eGFR", "Prior MI",
                       "Prior Stroke or TIA", "Prior Heart Failure", "Cardiovascular medication",
                       "T2DM medication", "Insulin", "Morbid obesity",
                       "First occurrence of Nonfatal myocardial infarction, nonfatal stroke, death from all cause",
                       "semaglutide treatment", "Semaglutide medication", "income", "musical taste"]]
}
