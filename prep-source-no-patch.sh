#!/bin/bash

set -xe

# Source info.
SPARK_COMMIT=1d27d7cf1e19633390beb92a9ea9f11ba601f773
WHY3_COMMIT=70ed0a8608a7a605e35ac14fdea723ccdf3e4e6e

# Remove any existing source dir.
rm -rf spark2014-$SPARK_COMMIT

# Unpack tarballs.
tar --extract --gzip --file spark2014-${SPARK_COMMIT:0:7}.tar.gz
tar --extract --gzip --file why3-${WHY3_COMMIT:0:7}.tar.gz

# Copy Why3 sources into the SPARK 2014 source tree.
rmdir spark2014-$SPARK_COMMIT/why3
mv why3-$WHY3_COMMIT spark2014-$SPARK_COMMIT/why3
