import importlib
import pkgutil

import drawthings_py


def test_all_modules_importable():
    """Every module in the package can be imported."""
    for module in pkgutil.walk_packages(
        drawthings_py.__path__,
        prefix=f"{drawthings_py.__name__}.",
    ):
        importlib.import_module(module.name)


def test_public_api():
    """Every name exported via __all__ exists."""
    assert len(drawthings_py.__all__) == len(set(drawthings_py.__all__))

    for name in drawthings_py.__all__:
        getattr(drawthings_py, name)
