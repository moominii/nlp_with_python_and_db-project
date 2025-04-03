# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:33:22 2025

@author: Jiyeon Baek

블로거들이 추천하는 서울 명소 분석하기 : 서울명소.txt
"""


import mysql.connector

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",   # MySQL 서버 주소 (원격이면 변경)
    user="root",  # MySQL 사용자명
    password="jiyeoun1",  # MySQL 비밀번호
    database="tourism_analysis"
)
cursor = conn.cursor()

# 파일 경로
stopwords_file = "C:/Users/Admin/Desktop/JY/Python/20250311/project/불용어 사전의 예/서울명소gsub.txt"
additional_words_file = "C:/Users/Admin/Desktop/JY/Python/20250311/project/사전 추가의 예/서울명소merge.txt"

# 불용어사전 삽입
with open(stopwords_file, "r", encoding="cp949") as f:
    stopwords = f.read().splitlines()

for word in stopwords:
    try:
        cursor.execute("INSERT IGNORE INTO stopwords (word) VALUES (%s)", (word,))
    except Exception as e:
        print(f"Error inserting {word}: {e}")

# 추가사전 삽입
with open(additional_words_file, "r", encoding="cp949") as f:
    additional_words = f.read().splitlines()

for word in additional_words:
    try:
        cursor.execute("INSERT IGNORE INTO additional_words (word) VALUES (%s)", (word,))
    except Exception as e:
        print(f"Error inserting {word}: {e}")

# 변경 사항 저장
conn.commit()

# 연결 종료
cursor.close()
conn.close()

print("데이터 삽입 완료!")


import pymysql
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import re

# 🔹 MySQL 연결 & 불용어 / 추가 단어 가져오기
def get_words_from_db():
    conn = pymysql.connect(host="localhost", user="root", password="jiyeoun1", database="tourism_analysis", charset="utf8")
    cursor = conn.cursor()

    # 🔹 불용어 가져오기
    cursor.execute("SELECT word FROM stopwords;")
    stopwords = {row[0] for row in cursor.fetchall()}  # set으로 저장 (중복 방지)

    # 🔹 추가 단어 가져오기
    cursor.execute("SELECT word FROM additional_words;")
    extra_words = {row[0] for row in cursor.fetchall()}  # set으로 저장

    conn.close()
    return stopwords, extra_words

# 🔹 MySQL에서 데이터 가져오기
stopwords, extra_words = get_words_from_db()



# 🔹 서울 명소 텍스트 파일 로드
def load_text(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        text_data = f.read()
    return text_data

text = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/서울명소.txt")  # 서울 명소 데이터



# 🔹 텍스트 전처리 함수
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = text.split()
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    words.extend(extra_words)  # 추가 단어 포함
    return words

# 🔹 정제된 단어 리스트
words = clean_text(text)


# 🔹 단어 빈도수 계산
word_counts = Counter(words)

# 🔹 WordCloud 생성 함수
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
generate_wordcloud(word_counts, "블로거들이 추천하는 서울 명소")






























