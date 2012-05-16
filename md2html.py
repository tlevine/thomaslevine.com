#!/usr/bin/env python2
import os
from lxml.html import fromstring, tostring
import sys

filename = sys.argv[1]

os.system('''/usr/bin/vendor_perl/Markdown.pl "%s" | sed -e 's/<!--.*-->//' > tmp.html ''' % filename)
html = fromstring(open('tmp.html').read())
for p in html.cssselect('p'):
    p.text = p.text.replace('\n', ' ')
os.system('rm tmp.html')

print tostring(html)[5:-6] #Remove the div tag
