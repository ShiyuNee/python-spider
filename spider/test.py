from bs4 import BeautifulSoup
import requests
import os
import re
import json
from token_test import *
from collections import defaultdict
from compute import compute_entropy, zip_law
import time
from selenium import webdriver  

# os.environ["http_proxy"] = "127.0.0.1:7890"
# os.environ["https_proxy"] = "127.0.0.1:7890"
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

def get_ch_book(url, out_path):
    root_url = url
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'} # chrome浏览器
    page_text=requests.get(root_url, headers=headers, timeout=5).content.decode()
    soup1=BeautifulSoup(page_text, 'lxml')
    res_list = []

    tag_list = soup1.find(class_='paiban').find_all(class_='menu-item')
    url_list = [item.find('a')['href'] for item in tag_list]
    print(url_list)
    for item in url_list:
        chapter_page = requests.get(item, headers=headers, timeout=5).content.decode()
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

def collect_data_ch(data_list: list):
    voc = defaultdict(int)
    for data in data_list:
        for idx in range(len(data)):
            filtered_data = filter_cn(data[idx]['text'])
            tokenized_data = tokenize(filtered_data)
            for item in tokenized_data:
                k = remove_punc(item)
                k = get_cn(k)
                if k != '':
                    voc[k] += 1
    write_jsonl([voc], './books/dict/ch_vocabulary.jsonl')
    return voc

def down_ope(url):
    driver = webdriver.Chrome()  # 根据需要选择合适的浏览器驱动  
    driver.get(url)  # 替换为你要爬取的网站URL  
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  
        time.sleep(5)
    return driver

def get_en_book(url, out_dir):
    root_url = url + '/en/books/en'
    headers={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36'} # chrome浏览器
    driver = down_ope(root_url)
    soup1=BeautifulSoup(driver.page_source, 'lxml')
    books = soup1.find_all(class_ = 'field-content')
    book_url = [item.a['href'] for item in books]
    for item in book_url:
        if item[-4:] != 'read':
            continue
        out_path = out_dir + item.split('/')[-2] + '.jsonl'
        time.sleep(2)
        try:
            book_text=requests.get(url + item, headers=headers).content.decode()
        except:
            continue
        soup2=BeautifulSoup(book_text, 'lxml')
        res_list = []
        sec_list = soup2.find_all('div', class_=re.compile('page n.*'))
        for sec in sec_list:
            res = ""
            sec_content = sec.find_all('p')
            for p_content in sec_content:
                text = p_content.text.strip()
                if text != '':
                    res += text
            print(res)
            res_list.append({'text': res})
        write_jsonl(res_list, out_path)
        
def collect_data_en(data_list: list):
    voc = defaultdict(int)
    for data in data_list:
        for idx in range(len(data)):
            tokenized_data = tokenize_en(data[idx]['text'])
            for item in tokenized_data:
                k = remove_punc(item)
                k = get_en(k)
                if k != '':
                    voc[k] += 1
    write_jsonl([voc], './books/dict/en_vocabulary.jsonl')
    return voc

def plot_en():
    # get_en_book('https://anylang.net', './books/en/')
    all_data = []
    for f_name in os.listdir('./books/en'):
        data = read_json('./books/en/' + f_name)
        all_data.append(data)
    voc_dict = collect_data_en(all_data[:60])
    # compute_entropy(voc_dict)
    # zip_law(voc_dict)

def plot_ch():
    all_data = []
    for f_name in os.listdir('./books/ch'):
        data = read_json('./books/ch/' + f_name)
        all_data.append(data)
    voc_dict = collect_data_ch(all_data)
    # compute_entropy(voc_dict)
    # zip_law(voc_dict)

plot_ch()