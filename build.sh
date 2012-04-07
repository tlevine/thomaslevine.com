#!/bin/bash

# Delete old version
rm -R www/publish

# Build the website
cd www/build
ant build
cd -

# Upload
scp -r www/publish/* www-data@thomaslevine.com:/srv/www/thomaslevine.com/www
