#!/bin/bash
FORMATS='atom rss-1.0 rdfxml'
INTERMEDIATE_DIR=../intermediate
PUBLISH_DIR=../publish

#Concatenate
mkdir -p $INTERMEDIATE_DIR/posts
cp posts/index.ttl $INTERMEDIATE_DIR/posts/index.ttl
sed \
  #Remove prefixes because they're aready in the aggregate ttl
  -e '/@prefix/d' \
  #Add redundant rss:link triples
  -e 's/^\(post:.*\)$/\1\n  rss:link \1 ;' \
  #Add a rss:channel ;
  -e '/^post:/ a "a rss:channel ;"' \
  posts/*/index.ttl > $INTERMEDIATE_DIR/posts/index.ttl

#Convert to triples
rapper -i turtle -o ntriples $INTERMEDIATE_DIR/posts/index.ttl > $INTERMEDIATE_DIR/posts/index.nt

#Add RSS and Atom entities
function feedtriple() {
  sourcetriple=$1
  newtriple=$2
  's/\([^ ]*\) \('$sourcetriple'\) \(.*\)$/\1 \2 \3\n\1 '$newtriple' \3/'
}
sed \
  -e "`feedtriple <http://thomaslevine.com/terms#title> <http://purl.org/rss/1.0/title>`"
  -e "`feedtriple <http://thomaslevine.com/terms#title> <http://purl.org/rss/1.0/title>`"

#Convert to the three output formats
#RSS and Atom are aggregated, so they use the intermediate directory.
rapper -i turtle -o rdfxml posts/index.ttl > $PUBLISH_DIR/posts/index.rdf
rapper -i ntriples -o rss-1.0 $INTERMEDIATE_DIR/posts/index.nt > $PUBLISH_DIR/posts/index.rss
rapper -i ntriples -o atom $INTERMEDIATE_DIR/posts/index.nt > $PUBLISH_DIR/posts/index.atom
