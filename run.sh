#! /bin/bash

cd "$(dirname $0)/../..";
ROOT_PATH=`pwd`

$ROOT_PATH/examples/paleo/prepare_data.sh
env JAVA_OPTS="-Xmx4g" sbt "run -c examples/paleo/application.conf"
