import jieba
import re
import string
import nltk

def filter_cn(text):
    a = re.sub(u"\\（.*?）|\\{.*?}|\\[.*?]|\\【.*?】|\\(.*?\\)", "", text)
    return a

def get_cn(text):
     return re.sub(u"[^\u4e00-\u9fa5]+","",text)

def get_en(text):
    return re.sub(r"[^a-zA-Z ]+", '', text)

def remove_punc(text):
    puncs = string.punctuation + "“”，。？、‘’：！；"
    new_text = ''.join([item for item in text if item not in puncs])
    return new_text

def tokenize(text):
    return jieba.cut(text)

def tokenize_en(text):
    sen_tok = nltk.sent_tokenize(text)
    word_tokens = [nltk.word_tokenize(item) for item in sen_tok]
    tokens = []
    for temp_tokens in word_tokens:
        for tok in temp_tokens:
            tokens.append(tok.lower())
    return tokens
    
