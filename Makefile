GEN_SCRIPT = scripts/generate_grpc_flatbuffers.sh
OUT_DIR = src/drawthings_py/generated/dt_grpc

.PHONY: all generate proto flatbuffers clean

all: generate

generate:
	$(GEN_SCRIPT)

proto flatbuffers: generate

clean:
	rm -rf $(OUT_DIR)/image_service
	find $(OUT_DIR) -maxdepth 1 -type f -name '*.py' ! -name '__init__.py' -delete
