#!/bin/bash
FORMATS='ntriples rdfxml atom rss-1.0 dot'
PUBLISH_DIR=../publish

#List the files
files=''
files+=`ls -d posts/*.ttl` || sleep 0
files+=`ls -d tags/*.ttl`  || sleep 0

#Process the files
for file in $files; do
  for format in $FORMATS; do
    if [[ $format = rss-1.0 ]];
      then extension=rss
    elif [[ $format = ntriples ]];
      then extension=nt
    elif [[ $format = rdfxml ]];
      then extension=rdf
    else
      extension=$format
    fi
    filebase="`basename $file .ttl`"
    rapper -i turtle -o $format $file > $PUBLISH_DIR/$filebase.$extension
  done
done

./buildindex.py posts
./buildindex.py tags
