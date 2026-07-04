import warnings
from .model_suggester import ModelSuggester


class SimpleModelSuggester(ModelSuggester):
    """
    Deprecated. Use ModelSuggester directly.

    SimpleModelSuggester is now a thin alias for ModelSuggester with no
    expertise_list — behaviour is identical.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "SimpleModelSuggester is deprecated. Use ModelSuggester directly. "
            "Pass no expertise_list to suggest_graph() for equivalent behaviour.",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)
