"""Compatibility package exposing generated code as `drawthings_py.grpc`.

This package re-exports the generated `dt_grpc` modules so they can be
imported as `drawthings_py.grpc.<module>` (for example
`drawthings_py.grpc.image_service`).
"""

from . import image_service  # re-export the image_service subpackage

__all__ = ["image_service"]
