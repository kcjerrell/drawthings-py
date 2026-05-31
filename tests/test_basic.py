from build.lib.dt_grpc import image_service
import pytest


def test_imports():
    """all modules are importable"""
    try:
        from drawthings_py import (
            cli_service,
            configs,
            drawthings_service,
            filename_pattern,
            grpc_service,
            image_buffer,
            metadata,
            preview_decoders,
            request_builder,
            _gen_config,
            _png_writer,
            _util,
        )
        from drawthings_py.generated.dt_grpc import (
            GenerationConfiguration,
            CompressionMethod,
            Control,
            ControlInputType,
            ControlMode,
            LoRA,
            LoRAMode,
            SamplerType,
            SeedMode,
            image_service
        )
    except ImportError as e:
        pytest.fail(f"Failed to import a required module: {e}")

def test_import_all():
    import drawthings_py

    for attr in drawthings_py.__all__:
        assert hasattr(drawthings_py, attr)