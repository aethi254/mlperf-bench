#!/bin/bash
# Clones the MLPerf reference implementation into external/
set -e
git clone https://github.com/mlcommons/inference.git external/mlperf-inference
cd external/mlperf-inference
git submodule update --init --recursive
