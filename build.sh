#!/bin/bash

# Delete old version
rm -R www/publish

# Build the home page
cd www/build
ant build
cd -

# Build the blog
./rss.py
mv rss www/publish
cp -R blog www/publish/!

# Upload
scp -r www/publish/* www-data@thomaslevine.com:/srv/www/thomaslevine.com/www
