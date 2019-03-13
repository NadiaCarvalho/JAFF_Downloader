# Import libraries
import argparse
import os
import re
import time
import urllib.request

import requests
from bs4 import BeautifulSoup
from lxml import html
from lxml.etree import tostring

parser = argparse.ArgumentParser()
parser.add_argument("url", help="url to download",
                type=str)
parser.add_argument("user", help="user of website",
                type=str)
parser.add_argument("password", help="password of website",
                type=str)

args = parser.parse_args()


# URLs
url = 'http://meryton.com/aha/index.php?'
login_url = url
current_stories_url = url + '?board=13.0'
complete_regency_stories_url = url + '?board=14.0'
complete_modern_stories_url = url + '?board=97.0'

session_requests = requests.session()
result = session_requests.get(login_url)
tree = html.fromstring(result.text)
authenticity_token = list(set(tree.xpath("//input[@name='auth_key']/@value")))[0]

payload = {
    "ips_username": args.user,
    "ips_password": args.password,
    "auth_key": authenticity_token
}
print(payload)

response = session_requests.post("http://meryton.com/aha/index.php?app=core&module=global&section=login&do=process", data=payload, headers = dict(referer=login_url))

#TODO