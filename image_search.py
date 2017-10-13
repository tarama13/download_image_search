# -*- coding: utf-8 -*-
import configparser
from urllib.parse import quote_plus
import json
import sys
import os
import hashlib
import requests

config = configparser.ConfigParser()
config.read('./config.ini')
search_url = 'https://www.googleapis.com/customsearch/v1?key={key}&cx={cx}&q={q}&num={num}&start={start}&searchType=image'

# search_word で検索した結果の画像のURLを返す
# 10枚 * n回実行
def get_image_urls(search_word, repeat_num):
    urls = []
    images_per_request = 10

    for i in range(repeat_num):
        url = search_url.format(
            key = config.get('google', 'api_key'),
            cx = config.get('google', 'custom_search_engine'),
            q = quote_plus(search_word),
            num = images_per_request,
            start = i * images_per_request + 1,
        )
        print(url)

        res = requests.get(url)
        data = json.loads(res.content.decode('utf-8'))

        for j in range(len(data["items"])):
            urls.append(data["items"][j]["link"])

    return urls


def download_image(base, urls):
    output_dir = "images/" + base
    os.makedirs(output_dir, exist_ok=True)

    for i in range(len(urls)):
        try:
            print(urls[i])
            ext = os.path.splitext(urls[i])[1].split("?%&")[0]
            image = requests.get(urls[i]).content # download
            file_name = output_dir + "/" + hashlib.md5(image).hexdigest() + ext; # md5 hash
            print("save as " + file_name);
            with open(file_name, "wb") as fout:
                fout.write(image)

        except:
            print("failed to download image")
            continue


if __name__ == '__main__':
    argvs = sys.argv
    if (len(argvs) != 4):
        print ("Usage: $ python " + argvs[0] + " [search_word] [repeat num] [save_name]")
        quit()

    urls = get_image_urls(argvs[1], int(argvs[2]))
    print("---- Get URL ---- ")
    download_image(argvs[3], urls)
