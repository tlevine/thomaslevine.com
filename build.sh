#!/bin/bash

#Build the feed
rapper -i turtle -o rdfxml feed.ttl > publish/feed.rdf
rapper -i turtle -o atom feed.ttl > publish/feed.atom
rapper -i turtle -o rss-1.0 feed.ttl > publish/feed.rss

#Build the tags
#rapper -i turtle -o rdfxml tags.ttl > publish/tags.rdf

#Build the website
cd www/build
ant build
cd -
