# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/3/16 15:52
# @Author : Zoe
# @File : urls.py
# @Software : PyCharm


from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import  views

urlpatterns = [
    path('', views.wordcloud),
    path('wordcloud',views.wordcloud,name='select_name1'),
    path('echarts', views.getecharts,name='select_name2'),
    path('analyse', views.analyse,name='select_name3'),
    path(r'emotionAnalyse', views.emotionAnalyse)
]
urlpatterns += staticfiles_urlpatterns()
