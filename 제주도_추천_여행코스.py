# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:27:32 2025

@author: Jiyeon Baek

제주도 추천 여행코스 찾기 : 제주도여행지.txt

"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pymysql
import re

# 🔹 MySQL 연결 & 불용어 가져오기
def get_stopwords_from_db():
    conn = pymysql.connect(host="localhost", user="root", password="jiyeoun1", database="travel_analysis", charset="utf8")
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM stopwords_jeju;")
    stopwords = {row[0] for row in cursor.fetchall()}  # set으로 저장

    conn.close()
    return stopwords

stopwords = get_stopwords_from_db()

# 🔹 텍스트 파일 불러오기
def load_text(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        text_data = f.read()
    return text_data

text = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/제주도 여행지.txt")  # 제주도 여행지 데이터

# 🔹 텍스트 전처리
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = text.split()
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    return words

words = clean_text(text)

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

# 🔹 워드클라우드 실행
generate_wordcloud(word_counts, "제주도 추천 여행지")





















