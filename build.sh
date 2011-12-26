#!/bin/bash

#Build the feed
cd feed
./build.sh
cd -

#Build the website
cd www/build
ant build
cd -
