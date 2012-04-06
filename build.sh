#!/bin/bash

#Build the website
cd www/build
ant build
cd -

#Build the feed
#mkdir -p www/publish/feed
#rapper -i turtle -o rdfxml feed/ttl > www/publish/feed/rdf
#rapper -i turtle -o rss-1.0 feed/ttl > www/publish/feed/rss
