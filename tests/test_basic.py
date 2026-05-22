import pytest

def test_imports():
    try:
        import dt_grpc
        import grpclib
        import betterproto
        import flatbuffers
    except ImportError as e:
        pytest.fail(f"Failed to import a required module: {e}")

def test_proto_compiled():
    try:
        from dt_grpc import image_service
        assert hasattr(image_service, "ImageGenerationServiceStub")
    except ImportError as e:
        pytest.fail(f"Failed to import generated proto modules: {e}")

def test_flatbuffers_compiled():
    try:
        from dt_grpc import GenerationConfiguration
    except ImportError as e:
        pytest.fail(f"Failed to import generated flatbuffers modules: {e}")
