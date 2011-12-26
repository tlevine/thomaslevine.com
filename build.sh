#!/bin/bash

#Build the feed
rapper -i turtle -o rdfxml feed/index.ttl > publish/feed/index.rdf

#Build the website
cd www/build
ant build
cd -
