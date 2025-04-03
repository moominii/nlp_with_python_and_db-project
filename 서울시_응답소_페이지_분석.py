# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:18:55 2025

@author: Jiyeon Baek

서울시 응답소 페이지 분석하기 : 서울시 응답소.txt
"""

import re 

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


from matplotlib import font_manager, rc 
import platform 


if platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname = path).get_name()
    rc('font', family = font_name)
elif platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
else:
    print('Check your OS system')

# 🔹 파일 불러오기
file_path = "C:/Users/Admin/Desktop/JY/Python/20250311/project/서울명소.txt"

# 🔹 텍스트 데이터 읽기
try:
    with open(file_path, "r", encoding="utf-8") as f:
        text_data = f.read()
except UnicodeDecodeError:
    with open(file_path, "r", encoding="cp949") as f:  # 또는 "euc-kr"
        text_data = f.read()

# 🔹 텍스트를 단어별로 분리
words = text_data.split()

# 🔹 단어 빈도수 계산
word_freq = Counter(words)

# 🔹 WordCloud 생성
wordcloud = WordCloud(
    font_path=path,  # Windows에서 적용할 한글 폰트 경로
    width=800,
    height=400,
    background_color="white",
    colormap="coolwarm"
).generate_from_frequencies(word_freq)

# 🔹 WordCloud 시각화
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

























































