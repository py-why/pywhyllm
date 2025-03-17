import pytest
import openai

from pywhyllm.suggesters.simple_model_suggester import SimpleModelSuggester
from example_variables import TEST_VARIABLES


class TestSimpleModelSuggester(object):

    def test_pairwise_relationship(self):
        # TODO: add suport for a smaller model than gpt-4 that can be loaded locally.
        with pytest.raises(openai.OpenAIError):
            modeler = SimpleModelSuggester('gpt-4')

        try:
            example1 = TEST_VARIABLES["example1"]
            with pytest.raises(AssertionError):
                result = modeler.suggest_pairwise_relationship(example1[0], example1[1])
                pytest.fail("AssertionError not raised when expected!")

            result = modeler.suggest_pairwise_relationship(example1[0], example1[1])
            print(result)
            assert result is None or len(result) > 0

        except Exception as e:
            pytest.fail(f"Unexpected exception occured: {str(e)}")
