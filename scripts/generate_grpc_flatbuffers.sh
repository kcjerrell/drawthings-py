#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA_DIR="${ROOT_DIR}/resources"
OUT_DIR="${ROOT_DIR}/src/drawthings_py/generated/dt_grpc"
PROTO_FILE="${SCHEMA_DIR}/imageService.proto"
FLATBUFFER_FILE="${SCHEMA_DIR}/config.fbs"

if command -v poetry >/dev/null 2>&1; then
  PYTHON_CMD=(poetry run python)
else
  PYTHON_CMD=(python3)
fi

if ! command -v flatc >/dev/null 2>&1; then
  echo "error: flatc is required to generate FlatBuffers code." >&2
  echo "Install it from https://flatbuffers.dev/ or your package manager." >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

mkdir -p "${OUT_DIR}/image_service"

echo "Generating gRPC client/server types from ${PROTO_FILE}..."
"${PYTHON_CMD[@]}" -m grpc_tools.protoc \
  -I "${SCHEMA_DIR}" \
  --python_betterproto_out="${TMP_DIR}" \
  "${PROTO_FILE}"

mv "${TMP_DIR}/__init__.py" "${OUT_DIR}/image_service/__init__.py"

echo "Generating FlatBuffers types from ${FLATBUFFER_FILE}..."
find "${OUT_DIR}" -maxdepth 1 -type f -name "*.py" ! -name "__init__.py" -delete
flatc --python --gen-onefile --python-typing --gen-object-api -o "${OUT_DIR}" "${FLATBUFFER_FILE}"
touch "${OUT_DIR}/__init__.py"

echo "Generated code in ${OUT_DIR}"
