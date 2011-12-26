#!/bin/bash
FORMATS='atom rss-1.0 rdfxml'
INTERMEDIATE_DIR=../intermediate
PUBLISH_DIR=../publish

#Concatenate
mkdir -p $INTERMEDIATE_DIR/posts
cp posts/index.ttl $INTERMEDIATE_DIR/posts/index.ttl
sed '/@prefix/d' posts/*/index.ttl > $INTERMEDIATE_DIR/posts/index.ttl

#Convert to triples
rapper -i turtle -o ntriples $INTERMEDIATE_DIR/posts/index.ttl > $INTERMEDIATE_DIR/posts/index.nt

#Add RSS and Atom entities

#Convert to the three output formats
#RSS and Atom are aggregated, so they use the intermediate directory.
rapper -i turtle -o rdfxml posts/index.ttl > $PUBLISH_DIR/posts/index.rdf
rapper -i ntriples -o rss-1.0 $INTERMEDIATE_DIR/posts/index.nt > $PUBLISH_DIR/posts/index.rss
rapper -i ntriples -o atom $INTERMEDIATE_DIR/posts/index.nt > $PUBLISH_DIR/posts/index.atom
