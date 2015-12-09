#!/usr/bin/env python3

import json
import sys
import copy

from bs4 import BeautifulSoup, SoupStrainer, diagnose

import urllib.request
import urllib.parse


search_url = "http://www.isbnsearch.org/isbn/"

full_url = search_url + '9780195003437'

bookinfo_filter = SoupStrainer("div")

page = urllib.request.urlopen(full_url)

soup = BeautifulSoup(page.read(), "html.parser", parse_only=bookinfo_filter)

# for label in soup.find_all('strong'):
#     if label.string == "Author:":
#         print(label.nextSibling.string)

print(soup.find_all('p', class_='pricelink')[5].a.contents)
