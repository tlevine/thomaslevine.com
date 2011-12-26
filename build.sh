#!/bin/bash

#Build the website
cd www/build
ant build
cd -

#Build the feed
mkdir -p www/publish/feed
rapper -i turtle -o rdfxml feed/index.ttl > www/publish/feed/index.rdf
