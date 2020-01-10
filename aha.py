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
login_url = 'http://meryton.com/aha/index.php?'
login_post_url = "http://meryton.com/aha/index.php?app=core&module=global&section=login&do=process"
url = args.url

session_requests = requests.session()
result = session_requests.get(login_url)
login_html = html.fromstring(result.text)
authenticity_token = list(set(login_html.xpath("//input[@name='auth_key']/@value")))[0]

payload = {
    "ips_username": args.user,
    "ips_password": args.password,
    "auth_key": authenticity_token
}

response = session_requests.post(login_post_url, data=payload, headers = dict(referer=login_url))

story_content = session_requests.get(url).content

tree = html.fromstring(story_content)

pages_xpath = "//*[@class='topic_controls']//text()"
pages = tree.xpath(pages_xpath)

if(len(pages) > 7):
    number_pages = pages[6].split(" ")[-2]
else:
    number_pages = 1

css_xpath = "//*[@id='full_version']"
css_selected = tree.xpath(css_xpath)


title_xpath = "//*[@class='ipsType_pagetitle']/text()" 
title = tree.xpath(title_xpath)
title = title[0].strip('\n')

author_xpath = "//*[@itemprop='creator']//*[@itemprop='name']/text()"
author_x = tree.xpath(author_xpath)
author = author_x[0]

title_x_y_path = "//*[@class='ipsType_pagetitle']//*[@class='desc']/text()" 
title_x_y = tree.xpath(title_x_y_path)
title_x_y = title_x_y[0]
    
xpath = "//*[@class='post_body']//*[@itemprop='commentText']//text()"

file_title = title + ".txt"
os.chdir("/Users/nadiacarvalho/Documents/Documents/FF/JAFF/files/")
file= open(file_title,'w')

file.write("<h1>" + title + "</h1>\n")
file.write("<h2>" + author + "</h2>\n")
file.write("<h3>" + title_x_y + "</h3>\n\n\n")

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