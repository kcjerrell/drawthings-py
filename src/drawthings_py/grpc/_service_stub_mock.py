# pyright: reportUnusedParameter=false

from collections.abc import AsyncIterator

from drawthings_py.generated.dt_grpc.image_service import (
    EchoReply,
    EchoRequest,
    FileExistenceResponse,
    FileListRequest,
    FileUploadRequest,
    HoursRequest,
    HoursResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
    PubkeyRequest,
    PubkeyResponse,
    UploadResponse,
)


class ImageGeneractionServiceStubMock:
    async def generate_image(
        self, image_generation_request: "ImageGenerationRequest"
    ) -> AsyncIterator[ImageGenerationResponse]:
        raise NotImplementedError()

    async def files_exist(
        self, file_list_request: "FileListRequest"
    ) -> "FileExistenceResponse":
        raise NotImplementedError()

    async def upload_file(
        self, file_upload_request_iterator: AsyncIterator[FileUploadRequest]
    ) -> AsyncIterator[UploadResponse]:
        raise NotImplementedError()

    async def echo(self, echo_request: "EchoRequest") -> "EchoReply":
        raise NotImplementedError()

    async def pubkey(self, pubkey_request: "PubkeyRequest") -> "PubkeyResponse":
        raise NotImplementedError()

    async def hours(self, hours_request: "HoursRequest") -> "HoursResponse":
        raise NotImplementedError()
