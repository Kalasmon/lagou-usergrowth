# -*- coding: utf-8 -*-

import pandas as pd

import jieba
import nltk

from wordcloud import WordCloud
import matplotlib.pyplot as plt


# 读取数据
lagou = pd.read_csv('./output/lagou.csv', encoding='gbk', index_col=False).iloc[:, 1:]


# 导入停用词表
with open('./asset/hit_stopwords.txt', encoding='utf8') as doc:
    #print(doc.read())
    stopwords = doc.read().split('\n')

user_stopwords = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '.', ',', '负责']

stopwords = set(stopwords + user_stopwords)


# 拆分工作描述
split_words = '任职资格|岗位要求|任职要求|工作要求|【我们对您期望】'

lagou['job_content'] = lagou.bt.str.split(split_words).str[0]
lagou['job_request'] = lagou.bt.str.split(split_words).str[1]


# 分词以及准备词组集合
# 调整 jieba 分词的词频
jieba.suggest_freq('K歌', True)
jieba.suggest_freq('工作职责', True)
jieba.suggest_freq('岗位描述', True)
jieba.suggest_freq('短视频', True)

job_content_words = lagou.job_content.apply(lambda x: [i for i in list(jieba.cut(x)) if i not in stopwords]).sum()
job_request_words = lagou.job_request.apply(lambda x: [i for i in list(jieba.cut(x)) if i not in stopwords]).sum()

job_content_text = ' '.join(job_content_words)
job_request_text = ' '.join(job_request_words)


# 词频统计
job_content_dist = nltk.FreqDist(job_content_words)
job_request_dist = nltk.FreqDist(job_request_words)

for word, frequency in job_content_dist.most_common(50):
    print(u'工作内容词频 {}：{}'.format(word, frequency))

print('')

for word, frequency in job_request_dist.most_common(50):
    print(u'工作要求词频 {}：{}'.format(word, frequency))


# 画词云图
font = "C:/Windows/Fonts/STFANGSO.ttf"

wc = WordCloud(background_color='white',
               font_path=font,
               max_words=500,
               width=1600,
               height=800)

# 生成工作内容图云
wc.generate(job_content_text)

plt.figure( figsize=(20,10))
plt.imshow(wc)
plt.axis('off')
# plt.show()
wc.to_file('./output/job_content.png')

# 生成工作要求图云
wc.generate(job_request_text)

plt.figure( figsize=(20,10))
plt.imshow(wc)
plt.axis('off')
wc.to_file('./output/job_request3.png')
