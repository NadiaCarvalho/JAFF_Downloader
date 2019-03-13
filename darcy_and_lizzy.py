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

# login_URLs
dl_url = 'https://forum.darcyandlizzy.com/index.php'
login_url = dl_url + '?action=login'
login_post_url = dl_url + '?action=login2'
url = args.url

session_requests = requests.session()

# Get login csrf token
login = session_requests.get(login_url)

login_html = html.fromstring(login.text)
hidden_inputs = login_html.xpath(r'//form//input[@type="hidden"]')
form = {x.attrib["name"]: x.attrib["value"] for x in hidden_inputs}

# Create payload
form["user"] = ""
form["passwrd"] = ""
form["cookielength"] = 60
form["cookieneverexp"] = "on"

response = session_requests.post(login_post_url, data=form, headers = dict(referer=login_url))

story_content = session_requests.get(url).content
#print(story_content)

tree = html.fromstring(story_content)

pages_xpath = "//*[@class='navPages']"
pages = tree.xpath(pages_xpath)

number_pages = len(pages)/2.0
if number_pages == 0:
    number_pages = 1

title_xpath = "//*[@class='catbg']/text()" 
title = tree.xpath(title_xpath)

title_x = title[6]
title_x = title_x.strip('\n')
title_x = title_x.strip('\t')
title_x = "".join(title_x.split(":")[1:])
title_x = "".join(title_x.split("-")[0])
title_x = "".join(title_x.split(",")[0])
title_x = " ".join(title_x.split(" ")[1:])

file_title = title_x + ".txt"

os.chdir("/Users/nadiacarvalho/Documents/Github/fanfiction_downloader")

if os.path.exists(file_title)==False:  
    create_file= open(file_title,'w')  #This is just to  create the file 
                                                  #in case it doesn't exist
    create_file.close()
file= open(file_title,'r+')

data= file.read()

for i in range(0,int(number_pages)):
    download_url = ".".join(url.split(".")[:-1]) + "." + str(i*2) + "0"
    story_content = session_requests.get(download_url).content
    story_tree = html.fromstring(story_content)
    xpath = "//*[contains(@id,'msg_') and @class='inner']//text()"
    page_posts = story_tree.xpath(xpath) 
    for j in range(0,len(page_posts)):
        if isinstance(page_posts[j],str):
            file.write(page_posts[j] + "\n\n")
        else:
            file.write(tostring(page_posts[j]) + "\n\n")


file.close() 
