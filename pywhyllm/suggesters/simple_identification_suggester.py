import guidance
from guidance import system, user, assistant, gen
import re
from inspect import cleandoc

class SimpleIdentificationSuggester:

    def __init__(self, llm=None):
        if llm is not None:
            if (llm == 'gpt-4'):
                self.llm = guidance.models.OpenAI('gpt-4')

    def suggest_iv(self, factors, treatment, outcome):
        lm = self.llm
        with system():
            lm += "You are a helpful assistant for causal reasoning."

        with user():
            prompt_str = f"""Which factors in {factors} might be valid instrumental variables for identifying the effect of {treatment} on {outcome}?

            List the factors that are possible instrumental variables in <iv> </iv> tags."""
            lm += cleandoc(prompt_str)
        with assistant():
            lm += gen("iv")

        ivs = lm['iv']
        ivs_list = re.findall(r'<iv>(.*?)</iv>', ivs)

        return ivs_list

    def suggest_backdoor(self, factors, treatment, outcome):
        lm = self.llm
        with system():
            lm += "You are a helpful assistant for causal reasoning."

        with user():
            prompt_str = f"""Which set or subset of factors in {factors} might satisfy the backdoor criteria for identifying the effect of {treatment} on {outcome}?

            List the factors satisfying the backdoor criteria enclosing the name of each factor in <backdoor> </backdoor> tags.
            """
            lm += cleandoc(prompt_str)
        with assistant():
            lm += gen("backdoors")

        backdoors = lm['backdoors']
        backdoors_list = re.findall(r'<backdoor>(.*?)</backdoor>', backdoors)

        return backdoors_list

    def suggest_frontdoor(self, factors, treatment, outcome):
        lm = self.llm
        with system():
            lm += "You are a helpful assistant for causal reasoning."

        with user():
            prompt_str = f"""Which set or subset of factors in {factors} might satisfy the frontdoor criteria for identifying the effect of {treatment} on {outcome}?

            List the factors satisfying the frontdoor criteria enclosing the name of each factor in <frontdoor> </frontdoor> tags.
            """
            lm += cleandoc(prompt_str)
        with assistant():
            lm += gen("frontdoors")

        frontdoors = lm['frontdoors']
        frontdoors_list = re.findall(r'<frontdoor>(.*?)</frontdoor>', frontdoors)

        return frontdoors_list
