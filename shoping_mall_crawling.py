from urllib.request import Request
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
import numpy as np
import time
import os
import random
import time

# url = "https://www.monki.com/en_gbp/index.html"
google_play_store = "https://play.google.com/store/apps/details?id=kr.co.petdoc.petdoc&hl=ko&gl=US&showAllReviews=true"
req = Request(google_play_store, headers={'User-Agent':'Mozila/5.0'})
webpage = urlopen(req)
soup = BeautifulSoup(webpage)

html_doc = """<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc, 'html.parser')
print('---all contents---')
print(soup.prettify())
print('---title-----')
print(soup.title)

