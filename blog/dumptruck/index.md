ScraperWiki Offline!
========
May 23, 2012

It rather annoying that you can only use the scraperwiki library
on a ScraperWiki instance; most of it could work fine elsewhere.

So I've pulled it out so you can use it offline. Well I've actually
only done it for Python so far. You can install it from PyPI.

    pip install scraperwiki_local

And then you can `import scraperwiki` in scripts run on your local
computer. The `scraperwiki.sqlite` component is powered by
[DumpTruck](http://dumptruck.io), which you can install independently
of `scraperwiki_local`.

    pip install dumptruck

### Differences

DumpTruck works a bit differently from (and better than) the hosted ScraperWiki,
library, and some of these are passed on to the scraperwiki_local library,
but the change shouldn't break much existing code. Here are two differences.

#### Complex cell values

What happens if you do this?

    import scraperwiki
    shopping_list = ['carrots', 'orange juice', 'chainsaw']
    scraperwiki.sqlite.save([], 'shopping_list': shopping_list)

On a ScraperWiki server, `shopping_list` is converted to its unicode
representation, which looks like this:

    [u'carrots', u'orange juice', u'chainsaw']

In the local version, it is encoded to JSON, so it looks like this:

    ["carrots","orange juice","chainsaw"]

And when you retrieve it, it comes back as a list rather than as a string.
And if it can't be encoded to JSON, you get an error.

#### Case-insensitive column names

SQL is less sensitive to case than Python. The following code works fine
in both versions of the library.

    In [1]: shopping_list = ['carrots', 'orange juice', 'chainsaw']

    In [2]: scraperwiki.sqlite.save([], {'shopping_list': shopping_list})

    In [3]: scraperwiki.sqlite.save([], {'sHOpPiNg_liST': shopping_list})

    In [4]: scraperwiki.sqlite.select('* from swdata')

    Out[4]: 
    [{u'shopping_list': [u'carrots', u'orange juice', u'chainsaw']},
     {u'shopping_list': [u'carrots', u'orange juice', u'chainsaw']}]

Note that the key in the returned data is 'shopping_list' and not
'sHOpPiNg_liST'; the database uses the first one that was sent.
Now let's retrieve the individual cell values.

    In [5]: data = scraperwiki.sqlite.select('* from swdata')

    In [6]: print([row['shopping_list'] for row in data])
    Out[6][[u'carrots', u'orange juice', u'chainsaw'], [u'carrots', u'orange juice', u'chainsaw']]

The code above works in both versions of the library, but the code below
only works in the local version; it raises a KeyError on the hosted version.

    In [7]: print(data[0]['Shopping_List'])
    Out[7][[u'carrots', u'orange juice', u'chainsaw']]

In the hosted version, `scraperwiki.sqlite.select` returns a list of ordinary
dictionaries. In the local version, `scraperwiki.sqlite.select` returns a list
of [special dictionaries](https://github.com/tlevine/dicti) that have
case-insensitive keys.

