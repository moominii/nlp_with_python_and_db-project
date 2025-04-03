# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:44:43 2025

@author: Jiyeon Baek

연설문 분석 후 WordCloud 생성하기 : 노무현대통령.txt

"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

# 🔹 연설문 파일 불러오기
file_path = "C:/Users/Admin/Desktop/JY/Python/20250311/project/노무현대통령.txt"

with open(file_path, "r", encoding="cp949") as f:
    text_data = f.read()

# 🔹 불용어 리스트 (주요 연설문에서 자주 반복되는 단어들 제거)
stopwords = {
    "국민", "여러분", "존경하는", "대통령", "대한민국", "우리", "저는", "정말", "것입니다",
    "이번", "모든", "해야", "할", "하는", "오늘", "한", "위한", "하고", "될"
}

# 🔹 텍스트 전처리
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = text.split()
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    return words

words = clean_text(text_data)

# 🔹 단어 빈도수 계산
word_counts = Counter(words)

# 🔹 WordCloud 생성
def generate_wordcloud(word_counts, title):
    wordcloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", 
                          background_color="white",
                          width=800, height=400).generate_from_frequencies(word_counts)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=16)
    plt.show()

# 🔹 WordCloud 실행
generate_wordcloud(word_counts, "노무현 대통령 연설문 키워드 분석")

































