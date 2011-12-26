#!/bin/bash
FORMATS='atom rss-1.0'
INTERMEDIATE_DIR=../intermediate
PUBLISH_DIR=../publish

#Concatenate the files
for dir in $INTERMEDIATE_DIR $PUBLISH_DIR; do 
  mkdir $dir/posts $dir/tags
  for subdir in . posts tags; do
    cp $subdir/index.ttl $dir/$subdir/index.ttl
    cat $subdir/*/index.ttl >> $dir/$subdir/index.ttl
  done
done

#Leaf rdfs
for file in "`ls -d {tags,posts}/*/index.ttl`"; do
  cat templates/header.ttl > $INTERMEDIATE_DIR/$file
  cat $file >> $INTERMEDIATE_DIR/$file
  rapper -i turtle -o rdfxml $INTERMEDIATE_DIR/$file > $PUBLISH_DIR/$file
done

#Process the files
for format in $FORMATS; do
  if [[ $format = rss-1.0 ]];
    then extension=rss
  else
    extension=$format
  fi
  rapper -i turtle -o $format $INTERMEDIATE_DIR/tags/index.ttl > $PUBLISH_DIR/tags/index.$extension
  rapper -i turtle -o $format $INTERMEDIATE_DIR/posts/index.ttl > $PUBLISH_DIR/posts/index.$extension
  cp $PUBLISH_DIR/posts/index.$extension $PUBLISH_DIR/feed.$extension
done
