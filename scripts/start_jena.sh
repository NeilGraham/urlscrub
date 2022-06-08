#!/bin/bash

JENA_VERSION="4.5.0"

set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";

if [ ! -d ./apache-jena-fuseki-$JENA_VERSION ]; then
    printf "\nApache Jena Fuseki is not yet installed.\n"

    $SCRIPT_DIR/install_jena.sh

fi

printf "\nStarting Apache Jena Fuseki.\n\n"

cd $SCRIPT_DIR/../database/apache-jena-fuseki-$JENA_VERSION

./fuseki-server