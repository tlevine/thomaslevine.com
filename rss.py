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
    if set('=') != set(f.readline()[:-1]):
        raise ValueError("The second line of %s contains characters other than equal-signs." % path)

    # Date
    dateline = f.readline()[:-1]
    if dateline.lower().strip() == 'draft':
        continue
    try:
        pubDate = datetime.datetime.strptime(dateline, '%B %d, %Y')
    except ValueError:
        params = (path, datetime.date.today().strftime('%B %d, %Y'))
        raise ValueError('The third line of %s should be either the word "Draft" or a date in this format: %s.' % params)

    # Optional categories line
    categoriesline = f.readline().strip()
    if len(categoriesline) >= 10 and categoriesline[0:10].lower() == 'categories':
        categories = categoriesline[10:].split(',')
        emptyline = f.readline().strip()
    elif '' == categoriesline:
        categories = []
        emptyline = categoriesline
    else:
        raise ValueError("The fourth line of %s should have a list of categories or be empty." % path)
     
    # Empty line
    if '' != emptyline:
        raise ValueError("There should be an empty line between the header and body inside %s." % path)

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
         categories = categories
    ))

rss = PyRSS2Gen.RSS2(
    title = "Thomas Levine",
    link = RSS,
    description = "Thomas Levine",
    lastBuildDate = datetime.datetime.utcnow(),
    items = items
)

rss.write_xml(open("rss", "w"))
