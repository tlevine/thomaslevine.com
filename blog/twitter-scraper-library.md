I wanted to save the tweets from [Transparency Camp](tcamp).
This prompted me to turn [Anna](annaps)'s [basic Twitter scraper](basic)
into a [library](twitter_search). Here's how you use it.

Import it. (It only works on ScraperWiki, unfortunately.)

    from scraperwiki import swimport
    search = swimport('twitter_search').search

Then search for terms.

    search(['picnic #tcamp12', 'from:TCampDC', '@TCampDC', '#tcamp12', '#viphack'])

A separate search will be run on each of these phrases.

### A more complete search
Searching for `#tcamp12` and `#viphack` didn't get me all of the
tweets because I waited like a week to do this. In order to get
a more complete list of the tweets, I looked at the tweets returned
from that first search; I searched for tweets referencing the users
who had tweeted those tweets.

    from scraperwiki.sqlite import save, select
    from time import sleep

    # Search by user to get some more
    users = [row['from_user'] + ' tcamp12' for row in \
        select('distinct from_user from swdata where from_user where user > "%s"' \
        % get_var('previous_from_user', ''))]
    
    for user in users:
        search([user], num_pages = 2)
        save_var('previous_from_user', user)
        sleep(2)

By default, the `search` function retrieves 15 pages of results, which
is the maximum. In order to save some time, I limited this second phase
of searching to two pages, or 200 results; I doubted that there would
be more than 200 relevant results mentioning a particular user.

The [full script](tcamp_tweets) also counts how many tweets were made
by each user.

### Library

Remember, this is a library, so you can easily reuse it in your own
scripts, like [Max Richman](max) has already [started doing](datahh_tweets).

[annaps]: https://scraperwiki.com/profiles/AnnaPS/
[basic]: https://scraperwiki.com/scrapers/basic_twitter_scraper/
[tcamp]: http://transparencycamp.org/
[twitter_search]: https://scraperwiki.com/scrapers/twitter_search/
[tcamp_tweets]: https://scraperwiki.com/scrapers/tcamp_tweets/
[datahh_tweets]: https://twitter.com/#!/datahh/status/198507824958013441
[max]: https://twitter.com/datahh/
