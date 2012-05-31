Handling exceptions in scrapers
========
April 17, 2012

When requesting and parsing data from a source with unknown properties
and random behavior (i.e., scraping), I expect all kinds of bizarrities to occur.
Managing exceptions is particularly helpful in such cases.

Here is some ways that an exception might be raised.

    [][0] #The list has no zeroth element, so this raises an IndexError
    {}['foo'] #The dictionary has no foo element, so this raises a KeyError

I would generally try to prevent the exception
from coming up in the first place,
but catching the exception might make sense.

Example 1: Inconsistant date formats
------
Let's say we're parsing dates.

    import datetime

This doesn't raise an error.

    datetime.datetime.strptime('2012-04-19', '%Y-%m-%d')

But this does.

    datetime.datetime.strptime('April 19, 2012', '%Y-%m-%d')

It raises a ValueError because the date formats don't match.
So what do we do if we're scraping a data source with multiple date formats?

### Ignoring unexpected date formats
A simple thing is to ignore the date formats that we didn't expect.

    import lxml.html
    import datetime

    def parse_date1(source):
        rawdate = lxml.html.fromstring(source).get_element_by_id('date').text

        try:
             cleandate = datetime.datetime.strptime(rawdate, '%Y-%m-%d')
        except ValueError:
             cleandate = None

        return cleandate

    print parse_date1('<div id="date">2012-04-19</div>')

If we make a clean date column in a database and put this in there,
we'll have some rows with dates and some rows with nulls. If there
are only a few nulls, we might just parse those by hand.

### Trying multiple date formats
Maybe we have determined that this particular data source uses
three different date formats. We can try all three.

    import lxml.html
    import datetime

    def parse_date2(source):
        rawdate = lxml.html.fromstring(source).get_element_by_id('date').text

        for date_format in ['%Y-%m-%d', '%B %d, %Y', '%d %B, %Y']:
            try:
                 cleandate = datetime.datetime.strptime(rawdate, date_format)
            except ValueError:
                 cleandate = None
            else:
                 break

        return cleandate

    print parse_date2('<div id="date">19 April, 2012</div>')

This loops through three different date formats and returns the first
one that doesn't raise the error.

Example 2: Unreliable HTTP connection
-----------
If you're scraping an unreliable website or you are behind
an unreliable internet connection, you may sometimes get
HTTPErrors or URLErrors for valid URLs. Trying again later
might help.

    import urllib2

    def load(url):
        retries = 3
        for i in range(retries):
            try:
                handle = urllib2.urlopen(url)
            except urllib2.URLError:
                if i + 1 == retries:
                    raise
                else:
                    time.sleep(42)
            else:
                break
        return handle.read()

    print load('http://thomaslevine.com')

This function tries thrice to download the page.
On the first two fails, it waits 42 seconds and tries again.
On the third failure, it raises the error.
On a success, it returs the content of the page.

Example 3: Logging errors rather than raising them
-----------
For more complicated parses, you might find loads
of errors popping up in weird places, so you might
want to go through all of the documents before deciding
which to fix first or whether to do some of them manually.

    import scraperwiki

    for document_name in document_names:
        try:
            parse_document(document_name)
        except Exception as e:
            scraperwiki.sqlite.save([], {
                'documentName': document_name,
                'exceptionType': str(type(e)),
                'exceptionMessage': str(e)
            }, 'errors')

This catches any exception raised by a particular document,
stores it in the database and then continues with the next document.
Looking at the database afterwards, you might notice some trends
in the errors that you can easily fix and some others where you
might hard-code the correct parse.

Example 4: Exiting gracefully
-----------

When I'm scraping over 9000 pages and my script fails
on page 8765, I like to be able to resume where I left off.
I can often figure out where I left off based on
the previous row that I saved to a database or file,
but sometimes I can't, particularly when I don't have
a unique index.

    for bar in bars:
        try:
            foo(bar)
        except:
            print('Failure at bar = "%s"' % bar)
            raise

This will tell me which bar I left off on.
It's fancier if I save the information to the database,
so here is how I might do that with ScraperWiki.

    import scraperwiki

    resume_index = scraperwiki.sqlite.get_var('resume_index', 0)
    for i, bar in enumerate(bars[resume_index:]):
        try:
            foo(bar)
        except:
            scraperwiki.sqlite.save_var('resume_index', i)
            raise
    scraperwiki.sqlite.save_var('resume_index', 0)

ScraperWiki has a limit on CPU time, so an error that often concerns me is the
[scraperwiki.CPUTimeExceededError](https://scraperwiki.com/docs/python/python_help_documentation/).
This error is raised after the script has used 80 seconds of CPU time;
if you catch the exception, you have two CPU seconds to clean up.
You might want to handle this error differently from other errors.

    import scraperwiki

    resume_index = scraperwiki.sqlite.get_var('resume_index', 0)
    for i, bar in enumerate(bars[resume_index:]):
        try:
            foo(bar)
        except scraperwiki.CPUTimeExceededError:
            scraperwiki.sqlite.save_var('resume_index', i)
            raise
        except Exception as e:
            scraperwiki.sqlite.save_var('resume_index', i)
            scraperwiki.sqlite.save([], {
                'bar': bar,
                'exceptionType': str(type(e)),
                'exceptionMessage': str(e)
            }, 'errors')
    scraperwiki.sqlite.save_var('resume_index', 0)

tl;dr
-------
Expect exceptions to occur when you are scraping a
randomly unreliable website with randomly inconsistent content,
and consider handling them in ways that allow the script
to keep running when one document of interest is bizarrely
formatted or not available.


