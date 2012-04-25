#!/bin/bash

if [ "$1" = deploy ]; then
  deploy=true
else
  deploy=false
fi

# Delete old version
rm -R www/publish

# Build the home page
cd www/build
ant build
cd -

# Build the blog
./feed.py
mv ! www/publish

if $deploy; then
  echo Uploading to thomaslevine.com
  scp -r www/publish/* www-data@thomaslevine.com:/srv/www/thomaslevine.com/www
else
  echo Not uploaded, but available locally at
  echo "`pwd`"/www/publish/index.html
  echo
  echo Run \`build.sh deploy\` to deploy after build.
fi
