#!/bin/bash
python -m grpc_tools.protoc -Iproto --python_out=. --grpc_python_out=. proto/number_guesser.proto
