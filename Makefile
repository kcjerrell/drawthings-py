PROTO_DIR = proto
OUT_DIR = src/dt_grpc

.PHONY: all proto flatbuffers clean

all: proto flatbuffers

proto:
	@echo "Compiling protobufs..."
	python -m grpc_tools.protoc -I $(PROTO_DIR) --python_betterproto_out=src $(PROTO_DIR)/imageService.proto
	@echo "Protobuf compilation complete."

flatbuffers:
	@echo "Compiling flatbuffers..."
	flatc --python -o $(OUT_DIR) $(PROTO_DIR)/config.fbs
	@echo "Flatbuffers compilation complete."

clean:
	rm -rf $(OUT_DIR)/image_service
	rm -rf $(OUT_DIR)/GenerationConfiguration
	rm -rf $(OUT_DIR)/*.py
	rm -rf $(OUT_DIR)/*/__pycache__
