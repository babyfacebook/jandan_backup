import os
import pickle as pkl
import re
import requests
import random
import urllib.request as ur
import argparse
from urllib.parse import urlparse
from core.requester import requester
from core.colors import good, info, run, green, red, white, end, bad
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm
from selenium.webdriver.chrome.options import Options
pa_id = re.compile(r'No.(\d+)')
pa_poster_id = re.compile(r'<b>(.+)</b> 发布于')
pa_text = re.compile(r'发布于.+\s+<p>((?!href).)+</p>')
pa_im_url = re.compile(r'src="//(.*\.jpg)')
pa_user = re.compile(r'<span class="">(.+?)</span>')
pa_comment = re.compile(r'class="tucao-content">(.+?)</div>')
pa_oo = re.compile(r'"tucao-oo">(\d+?)</span>')
pa_xx = re.compile(r'"tucao-xx">(\d+?)</span>')
th_urls = open('./jandan.net/internal.txt', 'r').readlines()
th_urls = [d.strip('\n') for d in th_urls if '/t/' in d and 'page' not in d and 'pond' not in d]
th_url_base = './data/th_rul_base.pkl'
sys.path.append('F:\\webdriver')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
browser = webdriver.Chrome(executable_path=r'F:\webdriver\chromedriver.exe',options=chrome_options)
browser.maximize_window()
if not os.path.exists(th_url_base):
    if not os.path.exists(os.path.dirname(th_url_base)):
        os.makedirs(os.path.dirname(th_url_base))
    collections = []
else:
    collections = pkl.load(open(th_url_base, 'wb'))
for th_url in tqdm(th_urls):
    if th_url in th_url_base:
        continue
    else:
        sess = dict()
        try:
            browser.get(th_url)
        except:
            continue
        content = browser.page_source
        id = re.findall(pa_id, content)
        poster_id = re.findall(pa_poster_id, content)
        text = re.findall(pa_text, content)
        im_url = re.findall(pa_im_url, content)
        if len(im_url) == 0 and len(text) == 0:
            continue
        if len(id) == 0 or len(text) == 0 or len(im_url) == 0 or len(poster_id) == 0:
            continue
        sess['id'] = id[0]
        sess['poster_id'] = poster_id[0]
        if len(text) == 0:
            sess['text'] = []
        else:
            sess['text'] = text[0]
        if len(im_url) == 0:
            sess['im_url'] = []
        else:
            sess['im_url'] = im_url[0]
        users = re.findall(pa_user, content)
        comments = re.findall(pa_comment, content)[:-1]
        oos = re.findall(pa_oo, content)
        xxs = re.findall(pa_xx, content)
        comm = []
        if len(users) == len(comments) and len(comments) == len(oos) and len(oos) == len(xxs):
            comm = [[users[i], comments[i], oos[i], xxs[i]] for i in range(len(users))]
        else:
            continue
        sess['comments'] = comm
        collections.append(sess)
pkl.dump(collections, open(th_url_base, 'wb'))

