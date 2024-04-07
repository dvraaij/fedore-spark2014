#!/bin/bash

set -xe

# Source info.
SPARK_COMMIT=ce5fad038790d5dc18f9b5345dc604f1ccf45b06
WHY3_COMMIT=fb4ca6cd8c7d888d3e8d281e6de87c66ec20f084

# Remove any existing source dir.
rm -rf spark2014-$SPARK_COMMIT

# Unpack tarballs.
tar --extract --gzip --file spark2014-${SPARK_COMMIT:0:7}.tar.gz
tar --extract --gzip --file why3-${WHY3_COMMIT:0:7}.tar.gz

# Copy Why3 sources into the SPARK 2014 source tree.
rmdir spark2014-$SPARK_COMMIT/why3
mv why3-$WHY3_COMMIT spark2014-$SPARK_COMMIT/why3
