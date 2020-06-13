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
login_url = 'https://meryton.com/aha/index.php?/login/'
url = args.url

session_requests = requests.session()
result = session_requests.get(login_url)
login_tree = html.fromstring(result.content)

csrf_xpath = "//*[@class='ipsBox_alt']/input[@name='csrfKey']/@value"
csrfKey = login_tree.xpath(csrf_xpath)[0]

payload = {
    "csrfKey": csrfKey,
    "auth": args.user,
    "password": args.password,
    "remember_me": 1,
    "_processLogin": 'usernamepassword',
    "_processLogin": 'usernamepassword',
}

response = session_requests.post(login_url, data=payload)

story_content = session_requests.get(url).content

tree = html.fromstring(story_content)

pages_xpath = "//*[@class='ipsPagination_pageJump']//text()"
pages = tree.xpath(pages_xpath)

if(len(pages) > 2):
    number_pages = pages[1].split(" ")[-2]
else:
    number_pages = 1

title_xpath = "//h1//text()"
title = tree.xpath(title_xpath)
title = title[2].strip('\n')

author_xpath = "//span[@class='ipsType_normal']//a//text()"
author_x = tree.xpath(author_xpath)
author = author_x[0]

description_xpath = "//span[@class='cTemplateField_value']//text()" 
description_x = tree.xpath(description_xpath)
description = description_x[2]
rating = description_x[5]
    #comment-745041_wrap > div:nth-child(2)
xpath = "//*[contains(concat(' ',normalize-space(@class),' '),'cPost_contentWrap')]//text()"

file_title = title + ".txt"
os.chdir("/Users/nadiacarvalho/Documents/Documents/FF/JAFF/files/")
file= open(file_title,'w')

file.write("<h1>" + title + "</h1>\n")
file.write("<h2>" + author + "</h2>\n")
file.write("<h3>" + description + "</h3>\n")
file.write("<h3>" + rating + "</h3>\n\n\n")

num_chapters = 1

for i in range(0,int(number_pages)):
    if "&st=" in url:
        download_url = "".join(url.split("&st=")[:-1]) + "&st=" + str(i*2) + "0"
    else:
        download_url = url + "&st=" + str(i*2) + "0"

    story_content = session_requests.get(download_url).content
    story_tree = html.fromstring(story_content)
    page_posts = story_tree.xpath(xpath) 

    for j in range(0,len(page_posts)):
        if isinstance(page_posts[j],str):
            file.write(page_posts[j])
        else:
            file.write(tostring(page_posts[j]))


file.close() 
