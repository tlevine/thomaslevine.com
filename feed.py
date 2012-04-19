#!/usr/bin/env python2
"Generate Thomas Levine's RSS feed"

import datetime
from feedformatter import Feed
import os
import shutil
import misaka
from cgi import escape

DOMAIN = "http://thomaslevine.com"
BLOG_DIR = '!'
BLOG_ROOT = DOMAIN + '/' + BLOG_DIR + '/'
NOW = datetime.datetime.utcnow()

def getpaths(sourcedir = 'blog'):
    "Find all markdown files"
    mdpaths = []
    otherpaths = []
    for dirname, dirnames, filenames in os.walk(sourcedir):
        for filename in filenames:
            # Select the markdown files.
            if filename[-3:] == '.md':
                mdpaths.append(os.path.join(dirname, filename))
            elif filename in ['rss', 'rss1', 'rss2', 'atom', 'opml']:
                raise ValueError('The file name "{0}" is reserved for the {0} feed.'.format(filename))
            else:
                otherpaths.append(os.path.join(dirname, filename))

    # Don't do anything with otherpaths yet.
    return mdpaths

def getfeed(paths):
    "Make feed items out of paths"
    unsortedItems = []
    unsortedDates = []
    for path in paths:
        # Close the file from the previous iteration
        try:
            f.close()
        except NameError:
            pass

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
        if pubDate > NOW:
            # Ignore dates in the future
            print('Skipping %s because its pubDate is in the future' % path)
            continue

        # Optional categories line
        categoriesline = f.readline().strip()
        if len(categoriesline) >= 12 and categoriesline[0:12].lower() == 'categories: ':
            categories = [category.strip() for category in categoriesline[12:].split(',')]
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
        try:
            description = misaka.html(f.read())
        except:
            print("Error parsing %s" % path)
            raise

        # Construct the link
        link = BLOG_ROOT + path

        # Append the item
        unsortedItems.append({
             'title': escape(title),
             'link': link,
             'guid': link,
             'description': escape(description),
             'pubDate': pubDate,
             'categories': categories
        })
        unsortedDates.append(pubDate)

    sortingHat = zip(unsortedDates, unsortedItems)
    sortingHat.sort(reverse = True)
    sortedDates, sortedItems = zip(*sortingHat)

    feed = Feed()
    feed.feed['title'] = "Thomas Levine"
    feed.feed['description'] = "Thomas Levine"
    feed.feed['lastBuildDate'] = NOW
    feed.feed['link'] = DOMAIN
    feed.feed['items'] = sortedItems

    return feed


def cleanup(outdir = BLOG_DIR):
    "Recreate the directory to which the blog will be published."

    try:
        shutil.rmtree(outdir)
    except OSError:
        pass #Directory doesn't exist

    os.mkdir(outdir)

def main():
    # Create the out directory
    cleanup()

    # Get markdown files
    paths = getpaths()

    # Copy them to the out directory
    for inpath in paths:
        outpath_tuple = (BLOG_DIR,) + os.path.split(inpath)[1:]
        outpath = os.path.join(*outpath_tuple)
        shutil.copy(inpath, outpath)

    # Make rss
    feed = getfeed(paths)
    feed.format_rss1_file(os.path.join('!', 'rss1'))
    feed.format_rss2_file(os.path.join('!', 'rss2'))
    feed.format_atom_file(os.path.join('!', 'atom'))

main()
