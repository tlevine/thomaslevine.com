#!/bin/bash
FORMATS='ntriples atom rss-1.0 dot'
PUBLISH_DIR=publish

for format in $FORMATS; do
  if [[ $format = rss-1.0 ]];
    then extension=rss
  elif [[ $format = ntriples ]];
    then extension=rdf
  else
    extension=$format
  fi
  rapper -i turtle -o $format index.turtle > $PUBLISH_DIR/index.$extension
done
