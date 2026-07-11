from grpclib import GRPCError, Status


class DrawThingsServerError(Exception):
    pass


class DrawThingsUnavailableError(Exception):
    pass


class InvalidDrawThingsResponseError(Exception):
    pass


def raise_grpc_error(e: GRPCError):
    if e.status == Status.INTERNAL:
        raise DrawThingsServerError(
            f"There was an error on the server. This could be a temporary issue with DT+ or a problem with your request. ({e.status.name}: {e.message})"
        ) from e

    if e.status == Status.UNAVAILABLE:
        raise DrawThingsUnavailableError(
            "The gRPC server is currently unavailable."
        ) from e
