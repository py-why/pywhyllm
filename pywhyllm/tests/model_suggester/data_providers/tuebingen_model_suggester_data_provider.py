# TESTS
variable = "water"
variable_a = "water intake"
description_a = "the amount of water a person drinks per day"
variable_b = "hydration level"
description_b = "the level of hydration in the body"
domain = "biology"

# MOCK_RESPONSES
test_suggest_description_expected_response = "<description>Water is a transparent, tasteless, odorless, nearly colorless liquid that is essential for all life forms and covers approximately 71% of Earth's surface, also existing in solid (ice) and gas (vapor) states.</description>"
test_suggest_onesided_relationship_expected_response = "<answer>A</answer>"
test_suggest_relationship_expected_response = "<answer>Yes</answer> <reference>Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. \"Water, hydration and health.\" Nutrition reviews 68.8 (2010): 439-458.</reference>"
# ASSERTIONS
test_suggest_description_expected_result = [
    "Water is a transparent, tasteless, odorless, nearly colorless liquid that is essential for all life forms and covers approximately 71% of Earth's surface, also existing in solid (ice) and gas (vapor) states."]
test_suggest_onesided_relationship_expected_result = 1
test__build_description_program_expected_result = {
    'system': 'You are a helpful assistant for writing concise and peer-reviewed descriptions. Your goal \n            is to provide factual and succinct description of the given concept.',
    'user': " Describe the concept of water.\n                    In one sentence, provide a factual and succinct description of water\n                        Let's think step-by-step to make sure that we have a proper and clear description. Then provide \n                        your final answer within the tags, <description></description>."}
test_suggest_relationship_expected_result = (1,
                                             [
                                                 'Popkin, Barry M., Kristen E. D\'Anci, and Irwin H. Rosenberg. "Water, hydration and health." Nutrition reviews 68.8 (2010): 439-458.'])
test__build_relationship_program_expected_result = {
    'system': 'You are a helpful assistant on causal reasoning and biology. Your goal is to answer \n            questions about cause and effect in a factual and concise way.',
    'user': "can changing water intake change hydration level? Answer Yes or No.At each step, each expert include a reference to a research paper that supports \n                    their argument. They will provide a one sentence summary of the paper and how it supports their argument. \n                        Then they will answer whether a change in water intake changes hydration level. Answer Yes or No.\n                        When consensus is reached, thinking carefully and factually, explain the council's answer. Provide \n                        the answer within the tags, <answer>Yes/No</answer>, and the most influential reference within \n                        the tags <reference>Author, Title, Year of publication</reference>.\n                        \n\n\n----------------\n\n\n<answer>Yes</answer>\n<reference>Author, Title, Year of \n                        publication</reference>\n\n\n----------------\n\n\n<answer>No</answer> {~/user}"}
