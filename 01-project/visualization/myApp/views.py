import json
import os

import keras
from django.shortcuts import render

import numpy as np
import  jieba.posseg as psg
import re
from keras.models import load_model
from gensim.models.word2vec import Word2Vec
from keras.preprocessing import sequence
import jieba

# Create your views here.

lists = {}

def wordcloud(request):
    return render(request, './html/wordcloud.html')

def getecharts(request):
    return render(request, './html/echarts.html')

def analyse(request):
    lists ['input']='此处请输入语句'
    lists['fenci'] = '此处为分词结果及词性标注'
    lists['dataclear'] = '此处为数据清洗结果'
    lists['emotion'] = '此处为情感分析结果'
    lists['emoji'] = 'emoji emoji1f308'
    return render(request, './html/analyse.html',{'lists':lists } )

def getClear(x):        # 去非中文符号
    line = x.strip()
    # 去除文本中的英文和数字
    line = re.sub("[a-zA-Z0-9]", "", line)
    # 去除文本中的中文符号和英文符号
    line = re.sub("[\s+\.\!\/_,$%^*(+\"\'；：“”．]+|[+——！，。？?、~@#￥%……&*（）]+", "", line)
    line = re.sub("【", "", line)
    return line


def emotionAnalyse(request):
    pwd = os.path.dirname(__file__)

    keras.backend.clear_session()
    
    # model = load_model(pwd + '\\6-bilstm_total-more.h5')
    # label = {0: "愤怒", 1: "恶心", 2: "开心", 3: "喜欢", 4: "中性", 5: "伤心"}
    # with open(pwd + '\\6-8-word2vec-more.json', "r", encoding="utf-8") as f:
    #     w2dic = json.load(f)

    model = load_model(pwd + '\\bilstm_total-more.h5')

    label = {0: "愤怒", 1: "厌恶", 2: "害怕", 3: "喜悦", 4: "喜欢", 5: "中性", 6: "低落", 7: "惊讶"}

    with open(pwd + '\\8-word2vec-more.json', "r", encoding="utf-8") as f:
        w2dic = json.load(f)

    if request.method == 'GET':
        in_str = request.GET.get("fname")
        lists['input'] = in_str
        in_stc = getClear(in_str)
        lists['dataclear'] = in_stc
        in_stc = psg.cut(in_stc)
        print(in_stc)
        int_word = []
        fenci = ""
        for w, t in in_stc:
            if w == " ":
                fenci += "  "
                continue
            fenci += w + "  /" + t + "  "
            int_word.append(w)
        lists['fenci'] = fenci

        new_txt = []
        data = []
        for word in int_word:
            try:
                new_txt.append(w2dic[word])
            except:
                new_txt.append(0)
        data.append(new_txt)

        print(data)
        data = sequence.pad_sequences(data, maxlen=150,padding='pre')
        print(data)
        pre = model.predict(data)[0].tolist()
        print("  ", label[pre.index(max(pre))])
        lists['emotion'] = label[pre.index(max(pre))]


        if pre.index(max(pre)) == 0:  # 愤怒
            lists['emoji'] = 'emoji emoji1f621'
        elif pre.index(max(pre)) == 1:  # 恶心
            lists['emoji'] = 'emoji emoji1f612'
        elif pre.index(max(pre)) == 2:  # 害怕
            lists['emoji'] = 'emoji emoji1f631'
        elif pre.index(max(pre)) == 3:  # 开心
            lists['emoji'] = 'emoji emoji1f604'
        elif pre.index(max(pre)) == 4:  # 喜欢
            lists['emoji'] = 'emoji emoji1f60d'
        elif pre.index(max(pre)) == 5:  # 中性
            lists['emoji'] = 'emoji emoji1f315'
        elif pre.index(max(pre)) == 6:  # 伤心
            lists['emoji'] = 'emoji emoji1f61e'
        else:  # 惊喜
            lists['emoji'] = 'emoji emoji1f61c'

        # if pre.index(max(pre)) == 0:  # 愤怒
        #     lists['emoji'] = 'emoji emoji1f621'
        # elif pre.index(max(pre)) == 1:  # 恶心
        #     lists['emoji'] = 'emoji emoji1f612'
        # elif pre.index(max(pre)) == 2:  # 开心
        #     lists['emoji'] = 'emoji emoji1f604'
        # elif pre.index(max(pre)) == 3:  # 喜欢
        #     lists['emoji'] = 'emoji emoji1f60d'
        # elif pre.index(max(pre)) == 4:  # 中性
        #     lists['emoji'] = 'emoji emoji1f315'
        # else:  # 伤心
        #     lists['emoji'] = 'emoji emoji1f61e'

        # if "过分" in lists['fenci']:
        #     lists['emotion'] = '愤怒'
        #     lists['emoji'] = 'emoji emoji1f621'
        #
        # if "可怕" in lists['fenci']:
        #     lists['emotion'] = '害怕'
        #     lists['emoji'] = 'emoji emoji1f631'
        #
        # if "竟然" in lists['fenci'] or "没想到" in lists['fenci']:
        #     lists['emotion'] = '惊喜'
        #     lists['emoji'] = 'emoji emoji1f61c'

    return render(request, './html/analyse.html', {'lists': lists})


# 太过分了，他怎么可以这样    我讨厌你    好可怕   这盆花真好看，好想买一盆回家
#我喜欢花      杯具就是这样产生的  我震惊了

