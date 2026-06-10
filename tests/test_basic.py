import pytest


def test_imports():
    """all modules are importable"""
    try:
        from drawthings_py import (  # noqa: F401
            cli_service,
            configs,
            filename_pattern,
            grpc_service,
            image_buffer,
            _metadata,
            _preview_decoders,
            request_builder,
            _png_writer,
            _util,
            drawthings,
            _dt_service,
            _errors,
        )
        from drawthings_py.generated.dt_grpc.config_generated import (  # noqa: F401
            GenerationConfiguration,
            CompressionMethod,
            Control,
            ControlInputType,
            ControlMode,
            LoRA,
            LoRAMode,
            SamplerType,
            SeedMode,
        )
        from drawthings_py.generated.dt_grpc.image_service import (
            ImageGenerationServiceStub,  # noqa: F401
        )
    except ImportError as e:
        pytest.fail(f"Failed to import a required module: {e}")


def test_import_all():
    import drawthings_py

    for attr in drawthings_py.__all__:
        assert hasattr(drawthings_py, attr)
