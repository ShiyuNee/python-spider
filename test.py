from bs4 import BeautifulSoup
import requests
import os
import re
import json
from token_test import *
from collections import defaultdict
from compute import compute_entropy, chef_theory

os.environ["http_proxy"] = "127.0.0.1:7890"
os.environ["https_proxy"] = "127.0.0.1:7890"
# 要爬取的小说主页

def read_json(path):
    qa_data = []
    f = open(path, 'r', encoding='utf-8')
    for line in f.readlines():
        qa_data.append(json.loads(line))
    return qa_data

def write_jsonl(data, path):
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    print(f'write jsonl to: {path}')
    f.close()

def get_book(url, out_path):
    # url = 'https://shuihu.5000yan.com/'
    # out_path = 'books/shuihu.jsonl'
    root_url = url
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'} # chrome浏览器
    page_text=requests.get(root_url, headers=headers).content.decode()
    soup1=BeautifulSoup(page_text, 'lxml')
    res_list = []

    tag_list = soup1.find(class_='paiban').find_all(class_='menu-item')
    url_list = [item.find('a')['href'] for item in tag_list]
    print(url_list)
    for item in url_list:
        chapter_page = requests.get(item, headers=headers).content.decode()
        chapter_soup = BeautifulSoup(chapter_page, 'lxml')
        res = ''
        try:
            chapter_content = chapter_soup.find(class_='grap')
        except:
            raise ValueError(f'no grap in the page {item}')
        chapter_text = chapter_content.find_all('div')
        print(chapter_text)
        for div_item in chapter_text:
            res += div_item.text.strip()
        res_list.append({'text': res})
    write_jsonl(res_list, out_path)

def collect_data(data_list: list):
    voc = defaultdict(int)
    for data in data_list:
        for idx in range(len(data)):
            filtered_data = filter_cn(data[idx]['text'])
            tokenized_data = tokenize(filtered_data)
            for item in tokenized_data:
                k = remove_punc(item)
                k = get_cn_and_number(k)
                if k != '':
                    voc[k] += 1
    return voc

data = read_json('./books/xiyouji.jsonl')
data2 = read_json('./books/shuihu.jsonl')
word_dic = collect_data([data])
chef_theory(word_dic)


