# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:13:17 2025

@author: Jiyeon Baek

여고생이 가장 고치고 싶은 성형부위 : 성형상담.txt

성형 수술 부작용 관련 키워드 분석 : 성형부작용.txt
"""


import pymysql

# MySQL 연결
conn = pymysql.connect(
    host="localhost", user="root", password="jiyeoun1", database="text_analysis", charset="utf8"
)
cursor = conn.cursor()

# 불용어 리스트 가져오기
cursor.execute("SELECT word FROM stopwords;")
stopwords = {row[0] for row in cursor.fetchall()}  # set으로 저장

# 추가 단어 리스트 가져오기
cursor.execute("SELECT word FROM extra_words;")
extra_words = {row[0] for row in cursor.fetchall()}  # set으로 저장

conn.close()  # 연결 종료

print("✅ 불용어:", stopwords)
print("✅ 추가 단어:", extra_words)


import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pymysql
import re


# 🔹 MySQL 연결 & 불용어, 추가 단어 가져오기
def get_words_from_db():
    conn = pymysql.connect(host="localhost", user="root", password="jiyeoun1", database="text_analysis", charset="utf8")
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM stopwords;")
    stopwords = {row[0] for row in cursor.fetchall()}

    cursor.execute("SELECT word FROM extra_words;")
    extra_words = {row[0] for row in cursor.fetchall()}

    conn.close()
    return stopwords, extra_words

stopwords, extra_words = get_words_from_db()




# 🔹 텍스트 파일 불러오기
def load_text(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        text_data = f.read()
    return text_data

text1 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/성형상담.txt")  # 여고생이 가장 고치고 싶은 성형부위
text2 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/성형부작용.txt")  # 성형 부작용

# 🔹 텍스트 전처리
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = text.split()
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    words.extend(extra_words)  # 추가 단어 포함
    return words

words1 = clean_text(text1)
words2 = clean_text(text2)

# 🔹 단어 빈도수 계산
word_counts1 = Counter(words1)
word_counts2 = Counter(words2)

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


generate_wordcloud(word_counts1, "여고생이 가장 고치고 싶은 성형부위")
generate_wordcloud(word_counts2, "성형 수술 부작용 관련 키워드")

















