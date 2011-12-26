#!/bin/bash
FORMATS='atom rss-1.0 rdfxml'
INTERMEDIATE_DIR=../intermediate
PUBLISH_DIR=../publish

#Concatenate the files
for dir in $INTERMEDIATE_DIR $PUBLISH_DIR; do 
  mkdir -p $dir/posts $dir/tags
  for subdir in . posts tags; do
    mkdir -p $dir/$subdir
    cp templates/header.ttl $dir/$subdir/index.ttl
    cat $subdir/index.ttl >> $dir/$subdir/index.ttl
    cat $subdir/*/index.ttl >> $dir/$subdir/index.ttl
  done
done

#Leaf rdfs
for file in `ls -d {tags,posts}/*/index.ttl`; do
  filedir="`echo $file|sed 's/index\.ttl$//'`"
  mkdir -p $INTERMEDIATE_DIR/$filedir $PUBLISH_DIR/$filedir

  filebase="`echo $file|sed 's/\.ttl$//'`"
  cp templates/header.ttl $INTERMEDIATE_DIR/$filebase.ttl
  cat $file >> $INTERMEDIATE_DIR/$filebase.ttl
  rapper -i turtle -o rdfxml $INTERMEDIATE_DIR/$filebase.ttl > $PUBLISH_DIR/$filebase.rdf
done

#Process the syndication feed files
for format in $FORMATS; do
  if [[ $format = rss-1.0 ]];
    then extension=rss
  elif [[ $format = rdfxml ]];
    then extension=rdf
  else
    extension=$format
  fi
  rapper -i turtle -o $format $INTERMEDIATE_DIR/tags/index.ttl > $PUBLISH_DIR/tags/index.$extension
  rapper -i turtle -o $format $INTERMEDIATE_DIR/posts/index.ttl > $PUBLISH_DIR/posts/index.$extension
#  cp $PUBLISH_DIR/posts/index.$extension $PUBLISH_DIR/feed.$extension
done
