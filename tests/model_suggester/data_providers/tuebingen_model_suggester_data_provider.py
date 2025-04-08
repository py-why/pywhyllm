# TESTS
variable = "water"
variable_a = "water intake"
description_a = "the amount of water a person drinks per day"
variable_b = "hydration level"
description_b = "the level of hydration in the body"
domain = "biology"

# MOCK_RESPONSES
test_suggest_description_expected_response = "<description>Water is a transparent, tasteless, odorless, nearly colorless liquid that is essential for all life forms and covers approximately 71% of Earth's surface, also existing in solid (ice) and gas (vapor) states.</description>"
test_suggest_onesided_relationship_a_cause_b_expected_response = "<answer>A</answer>"
test_suggest_onesided_relationship_a_not_cause_b_expected_response = "<answer>B</answer>"
test_suggest_relationship_a_cause_b_expected_response = "<answer>Yes</answer> <reference>Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. \"Water, hydration and health.\" Nutrition reviews 68.8 (2010): 439-458.</reference>"
test_suggest_relationship_a_not_cause_b_expected_response = "<answer>No</answer> <reference>Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. \"Water, hydration and health.\" Nutrition reviews 68.8 (2010): 439-458.</reference>"

# ASSERTIONS
test_suggest_description_expected_result = ([
                                                "Water is a transparent, tasteless, odorless, nearly colorless liquid that is essential for all life forms and covers approximately 71% of Earth's surface, also existing in solid (ice) and gas (vapor) states."],
                                            [])
test_suggest_onesided_relationship_a_cause_b_expected_result = 1
test_suggest_onesided_relationship_a_not_cause_b_expected_result = 0
test__build_description_program_no_context_no_reference_expected_result = {
    'system': 'You are a helpful assistant for writing concise and peer-reviewed descriptions. Your goal \nis to provide factual and succinct description of the given concept.',
    'user': "Describe the concept of water.\nIn one sentence, provide a factual and succinct description of water.\nLet's think step-by-step to make sure that we have a proper and clear description. Then provide \nyour final answer within the tags, <description></description>."}
test__build_description_program_no_context_with_reference_expected_result = {
    'system': 'You are a helpful assistant for writing concise and peer-reviewed descriptions. Your goal \nis to provide factual and succinct description of the given concept.',
    'user': 'Describe the concept of water.\nIn one sentence, provide a factual and succinct description of water.\nThen provide two research papers that support your description.\nLet\'s think step-by-step to make sure that we have a proper and clear description. Then provide \nyour final answer within the tags, <description></description>, and each research paper within the \ntags <paper></paper>.'}
test__build_description_program_with_context_with_reference_expected_result = {
    'system': 'You are a helpful assistant for writing concise and peer-reviewed descriptions. Your goal is \nto provide factual and succinct descriptions related to the given concept and context.',
    'user': "Using this context about the particular variable, describe the concept of water.\nIn one sentence, provide a factual and succinct description of water. Then provide two research papers that support your description.\nLet's think step-by-step to make sure that we have a proper and clear description. Then provide your final \nanswer within the tags, <description></description>, and each research paper within the tags <reference></reference>."}
test__build_description_program_with_context_no_reference_expected_result = {
    'system': 'You are a helpful assistant for writing concise and peer-reviewed descriptions. Your goal is \nto provide factual and succinct descriptions related to the given concept and context.',
    'user': "Using this context about the particular variable, describe the concept of water.\nIn one sentence, provide a factual and succinct description of water.\nLet's think step-by-step to make sure that we have a proper and clear description. Then provide your final \nanswer within the tags, <description></description>."}
test_suggest_relationship_a_cause_b_expected_result = (1,
                                                       [
                                                           'Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. "Water, hydration and health." Nutrition reviews 68.8 (2010): 439-458.'])
test_suggest_relationship_a_not_cause_b_expected_result = (0,
                                                           [
                                                               'Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. "Water, hydration and health." Nutrition reviews 68.8 (2010): 439-458.'])
test__build_relationship_program_expected_result = {
    'system': 'You are a helpful assistant on causal reasoning and biology. Your '
              'goal is to answer \n'
              'questions about cause and effect in a factual and '
              'concise way.',
    'user': 'can changing water intake change hydration level? Answer Yes or '
            'No.When consensus is reached, thinking carefully and factually, '
            "explain the council's answer. \n"
            '                    Provide the answer within the tags, '
            '<answer>Yes/No</answer>.\n'
            '                        \n'
            '\n'
            '\n'
            '----------------\n'
            '\n'
            '\n'
            '<answer>Yes</answer>\n'
            '\n'
            '\n'
            '----------------\n'
            '\n'
            '\n'
            '<answer>No</answer>'}
