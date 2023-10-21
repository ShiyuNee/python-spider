import jieba
import re
import string

def filter_cn(text):
    a = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】|\\(.*?\\)", "", text)
    return a

def get_cn_and_number(text):
     return re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039])","",text)

def remove_punc(text):
    puncs = string.punctuation + "“”，。？、‘’：！；"
    new_text = ''.join([item for item in text if item not in puncs])
    return new_text

def tokenize(text):
    return jieba.cut(text)

