from typing_extensions import override


class ReprMixin:
    @override
    def __repr__(self):

        fields = ", ".join(f"{k}={v!r}" for k, v in vars(self).items())  # pyright: ignore[reportAny]

        return f"{type(self).__name__}({fields})"
