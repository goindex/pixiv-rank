#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
import requests
import linecache
from pixivpy3 import *

if sys.version_info >= (3, 0):
    import importlib
    importlib.reload(sys)
else:
    reload(sys)
    sys.setdefaultencoding('utf8')
sys.dont_write_bytecode = True

_REFRESH_TOKEN = "YOUR TOKEN"
_TEST_WRITE = False

def make_dir():
    if not os.path.dirname(__file__):
        pass
    else:
        os.chdir(os.path.dirname(__file__))

    if not os.path.exists('./tmp'):
        os.makedirs('./tmp')

def create_html(aapi):
    def status_code(url):
        url_status_code = requests.head(url).status_code
        requests.session().keep_alive = False
        return url_status_code

    def create_temp_html(id, title, author, image_urls):
        image_id = str(id)
        image_title = str(title)
        image_author = str(author)
        image_large = str(image_urls.replace('i.pximg.net', 'www.lollipop.workers.dev'))
        image_original_temp = str(image_large.replace('/c/600x1200_90_webp/img-master', '/img-original'))
        image_original = str(image_original_temp.replace('_master1200', ''))
        if status_code(image_original) == 404:
            image_original = str(image_original_temp.replace('_master1200.jpg', '.png'))
        main_temp_html = open('./tmp/main_temp.html', 'a')
        main_temp_html.write('<article class="thumb"> ')
        main_temp_html.write('<a href="' + image_original + '" class="image lazyload" data-src="' + image_large + '" ')
        main_temp_html.write('<img class="lazyload" data-src="' + image_large + '" alt="' + image_title + '"> ')
        main_temp_html.write('</a> ')
        main_temp_html.write('<h2>' + image_title + '</h2> ')
        main_temp_html.write('<p>' + image_author + ' - <a href="https://pixiv.net/i/' + image_id + '" target="_blank">pixiv.net/i/' + image_id + '</a></p> ')
        main_temp_html.write('</article>\n')
        main_temp_html.close()

    def return_temp_html(amount):
        for index in range(amount):
            illust = json_result.illusts[index]
            create_temp_html(illust.id, illust.title, illust.user.name, illust.image_urls['large'])

    json_result = aapi.illust_ranking('day')
    illust_amount = len(json_result.illusts)
    return_temp_html(illust_amount)

    while True:
        illust_temp = illust_amount

        next_qs = aapi.parse_qs(json_result.next_url)
        json_result = aapi.illust_ranking(**next_qs)
        illust_amount = len(json_result.illusts)
        return_temp_html(illust_amount)

        illust_amount += illust_temp

        if illust_amount >= 150:
            break
        else:
            continue

    for line_number in range(1, 151):
        main_html = open('./tmp/main.html', 'a')
        main_html.write(linecache.getline('./tmp/main_temp.html', line_number).strip() + ' ')
        main_html.close()

    main_tpl = open('./tmp/main.html', 'r')
    main_tpl_html = main_tpl.read()
    main_tpl.close()
    template_tpl = open('./tpl/template.html', 'r')
    template_tpl_html = template_tpl.read()
    template_tpl.close()
    index_html = open('./dist/index.html', 'w')
    index_html.write(template_tpl_html.replace('{{main}}', main_tpl_html))
    index_html.close()

def remove_dir():
    if os.path.exists('./tmp'):
        shutil.rmtree('./tmp')

def main():
    aapi = AppPixivAPI()
    aapi.auth(refresh_token=_REFRESH_TOKEN)
    make_dir()
    create_html(aapi)
    remove_dir()

if __name__ == '__main__':
    main()
