#!/bin/bash

JENA_VERSION="4.5.0"

set -e

SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
cd $SCRIPT_DIR/../database

if [ ! -d ./apache-jena-fuseki-$JENA_VERSION ]; then
    printf "\nDownloading Jena Fuseki $JENA_VERSION.\n"

    curl https://dlcdn.apache.org/jena/binaries/apache-jena-fuseki-$JENA_VERSION.zip -o ./apache-jena-fuseki-$JENA_VERSION.zip

    unzip apache-jena-fuseki-$JENA_VERSION.zip

    printf "\nSuccessfully installed Apache Jena Fuseki $JENA_VERSION!\n\n"
    
else
    printf "\nApache Jena Fuseki $JENA_VERSION is already installed.\n\n"
fi



