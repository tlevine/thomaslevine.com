#!/bin/bash
FORMATS='ntriples rdfxml atom rss-1.0 dot'
PUBLISH_DIR=../publish

#List the files
files="index.ttl posts/index.ttl tags/index.ttl"
files+=" `ls -d posts/*/index.ttl`" || sleep 0
files+=" `ls -d tags/*/index.ttl`"  || sleep 0

mkdir $PUBLISH_DIR/posts $PUBLISH_DIR/tags

#Process the files
for file in $files; do
  filebase="`echo $file| sed s/\.ttl$//`"
  dir="`echo $file| sed s/index\.ttl$//`"
  mkdir $PUBLISH_DIR/$dir

  for format in $FORMATS; do
    echo $file $format ----------------------
    if [[ $format = rss-1.0 ]];
      then extension=rss
    elif [[ $format = ntriples ]];
      then extension=nt
    elif [[ $format = rdfxml ]];
      then extension=rdf
    else
      extension=$format
    fi
    rapper -i turtle -o $format $file > $PUBLISH_DIR/$filebase.$extension
  done
done

#./buildindex.py posts
#./buildindex.py tags
