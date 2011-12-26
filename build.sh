#!/bin/bash

#Build the feed
cd feed
./build.sh
cd -

#Build the website
cd www/build
ant build
cd -

#Convert the RDF for the website
rapper -i turtle -o ntriples www/index.ttl > publish/index.rdf
