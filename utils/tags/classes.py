import warnings


def experimental(cls):
    """Decorator that marks classes as experimental and warns upon their instantiation."""

    class ExperimentalClass(cls):
        def __init__(self, *args, **kwargs):
            warnings.warn(f"{cls.__name__} is experimental and may change in the future.", FutureWarning)
            super().__init__(*args, **kwargs)

    return ExperimentalClass
