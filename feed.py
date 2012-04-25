#!/usr/bin/env python2
"Generate Thomas Levine's RSS feed"

import datetime
from feedformatter import Feed
import os
import shutil
import misaka
from cgi import escape
from lxml.html import parse, tostring
from lxml import etree

# URIs
DOMAIN = "http://thomaslevine.com"
BLOG_DIR = '!'
BLOG_ROOT = DOMAIN + '/' + BLOG_DIR + '/'

# Other constants
FEED_FILES = ['rss', 'rss1', 'rss2', 'atom', 'opml']
NOW = datetime.datetime.now().timetuple()

def getpaths(sourcedir = 'blog'):
    "Find all markdown files"
    mdpaths = []
    otherpaths = []
    for dirname, dirnames, filenames in os.walk(sourcedir):
        for filename in filenames:
            # Select the markdown files.
            if filename[-3:] == '.md':
                mdpaths.append(os.path.join(*([dirname] + dirnames + [filename])))
            elif filename in FEED_FILES:
                raise ValueError('The file name "{0}" is reserved for the {0} feed.'.format(filename))
            else:
                otherpaths.append(os.path.join(dirname, filename))

    # Don't do anything with otherpaths yet.
    print mdpaths
    return mdpaths

def full_path_split(path, sourcedir = 'blog'):
    "Split a path into a list of single directories and files"
    parent = path
    dirs = []
    while parent != sourcedir:
        parent, current = os.path.split(parent)
        dirs.insert(0, current)
    return dirs

def getfeed(paths, sourcedir = 'blog'):
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
        title = f.readline()[:-1]

        # h1
        if set('=') != set(f.readline()[:-1]):
            raise ValueError("The second line of %s contains characters other than equal-signs." % path)

        # Date
        dateline = f.readline()[:-1]
        if dateline.lower().strip() == 'draft':
            continue
        try:
            pubDate = datetime.datetime.strptime(dateline, '%B %d, %Y').timetuple()
        except ValueError:
            params = (path, datetime.date.today().strftime('%B %d, %Y'))
            raise ValueError('The third line of %s should be either the word "Draft" or a date in this format: %s.' % params)
        if pubDate > NOW:
            # Ignore dates in the future
            print('Skipping %s because its pubDate is in the future' % path)
            continue

        # Optional categories line
        categoriesline = f.readline().strip()
        if len(categoriesline) >= 12 and categoriesline[0:12] == 'Categories: ':
            categories = [category.strip() for category in categoriesline[12:].split(',')]
            emptyline = f.readline().strip()
        elif '' == categoriesline:
            categories = []
            emptyline = categoriesline
        else:
            raise ValueError('The fourth line of %s should say "Categories: " and then list of categories or be empty.' % path)
         
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
        dirs = full_path_split(path, sourcedir = sourcedir)
        link = os.path.join(BLOG_ROOT, *dirs)

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
    feed.items = sortedItems

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
    for infile in paths:
        outfile_list = [BLOG_DIR] + full_path_split(infile, sourcedir = '')[1:]
        outfile = os.path.join(*outfile_list)
        outdir = os.path.join(*outfile_list[:-1])
        os.mkdir(outdir)
        shutil.copy(infile, outfile)

    # Make feed
    feed = getfeed(paths)

    # Render in feed formats
    feed.format_rss1_file(os.path.join('!', 'rss1'))
    feed.format_rss2_file(os.path.join('!', 'rss2'))
    feed.format_atom_file(os.path.join('!', 'atom'))

    # Render as HTML, using the home page as a template
    filename = os.path.join('www', 'publish', 'index.html')
    html = parse(filename).getroot()
    wrap = html.get_element_by_id('wrap')
    #wrap.remove(wrap.get_element_by_id('card'))
    wrap.remove(wrap.get_element_by_id('smallcards'))
    for stylesheet in html.xpath('//link[@rel="stylesheet"]'):
        href = '../' + stylesheet.attrib['href']
        stylesheet.attrib['href'] = href 

    img = html.cssselect('#card .logo img')[0]
    img.attrib['src'] = '../' + img.attrib['src']

    for script in html.cssselect('script'):
        if script.attrib.get('src', '       ')[:2] == 'js':
            script.attrib['src'] = '../' + script.attrib['src']

    # Add the feeds
    feedcard = etree.SubElement(wrap, 'div')
    feedcard.attrib['id'] = 'table-of-contents'
    feedcard.attrib['class'] = 'bigcard card'
    h2 = etree.SubElement(feedcard, 'h2')
    h2.text = 'Posts'
    ul = etree.SubElement(feedcard, 'ul')
    for item in feed.items:
        li = etree.SubElement(ul, 'li')
        a = etree.SubElement(li, 'a')
        a.attrib['href'] = item['link'].replace(BLOG_ROOT, '')
        a.text = item['title']

    # Write
    f = open(os.path.join('!', 'index.html'), 'w')
    f.write(tostring(html))
    f.close()

main()
