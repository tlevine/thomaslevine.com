#!/usr/bin/env python2
"Generate Thomas Levine's RSS feed"

import datetime
import PyRSS2Gen
import os
import misaka
from cgi import escape

DOMAIN = "http://thomaslevine.com"
RSS = DOMAIN + "/rss"
BLOG_ROOT = DOMAIN + "/!/"

# Find all markdown files
paths = []
for dirname, dirnames, filenames in os.walk('blog'):
    for filename in filenames:
        # Select the markdown files.
        if filename[-3:] == '.md':
            paths.append(os.path.join(dirname, filename))

# Make items out of them
items = []
for path in paths:
    f = open(path, 'r')

    # Title
    title = f.readline()

    # h1
    if set('=') != f.readline()[:-1]:
        raise ValueError("The second line of %s contains characters other than equal-signs." % path)

    # Date
    try:
        pubDate = datetime.datetime.strptime(f.readline()[-1], '%B %d, %Y').date()
    except ValueError:
        params = (path, datetime.date.today().strftime('%B %d, %Y'))
        raise ValueError("The third line of %s should contain a date in this format: %s." % params)

    # Empty line
    if '' != f.readline().strip():
        raise ValueError("The fourth line of %s should be empty, but it contains something." % path)

    # Description
    description = misaka.html(f.read())

    # Close the file
    f.close()

    # Construct the link
    link = BLOG_ROOT + path

    # Append the item
    items.append(PyRSS2Gen.RSSItem(
         title = escape(title),
         link = link,
         guid =  PyRSS2Gen.Guid(link),
         description = escape(description),
         pubDate = pubDate,
    ))

rss = PyRSS2Gen.RSS2(
    title = "Thomas Levine",
    link = RSS,
    description = "Thomas Levine",
    lastBuildDate = datetime.datetime.utcnow(),
    items = items
)

rss.write_xml(open("rss", "w"))
