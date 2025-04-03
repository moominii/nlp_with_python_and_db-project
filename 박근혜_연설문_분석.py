# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:48:03 2025

@author: Jiyeon Baek

대통령 신년 연설문 분석으로 정책 변화 예측하기 : 박근혜대통령취임사_2013.txt
                                              박근혜대통령신년연설물_2014_01_06.txt
                                              박근혜대통령신년연설물_2015_01_12.txt
"""

import pymysql
import pandas as pd
import re

# 🔹 MySQL에서 불용어 가져오기
def get_stopwords_from_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="jiyeoun1",
        database="speech_analysis",
        charset="utf8"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM stopwords;")
    stopwords = {row[0] for row in cursor.fetchall()}  # set으로 저장하여 중복 제거

    conn.close()
    return stopwords

stopwords = get_stopwords_from_db()

# 🔹 연설문 불러오기
def load_text(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        text_data = f.read()
    return text_data

text_2013 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령취임사_2013.txt")
text_2014 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령신년연설문_2014_01_06.txt")
text_2015 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령신년연설문_2015_01_12.txt")


from konlpy.tag import Okt

okt = Okt()

# 🔹 텍스트 정제 함수
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = okt.nouns(text)  # 명사 추출
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    return " ".join(words)  # 띄어쓰기로 구분된 문자열 반환

# 🔹 연설문 전처리
cleaned_2013 = clean_text(text_2013)
cleaned_2014 = clean_text(text_2014)
cleaned_2015 = clean_text(text_2015)

# 🔹 데이터프레임 생성
df = pd.DataFrame({
    "Year": [2013, 2014, 2015],
    "Speech": [cleaned_2013, cleaned_2014, cleaned_2015]
})

df.head()


from sklearn.feature_extraction.text import TfidfVectorizer

# 🔹 TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=50)  # 상위 50개 키워드 추출
tfidf_matrix = vectorizer.fit_transform(df["Speech"])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# 🔹 연도별 상위 TF-IDF 키워드 추출
top_keywords_2013 = tfidf_df.iloc[0].nlargest(10).index.tolist()
top_keywords_2014 = tfidf_df.iloc[1].nlargest(10).index.tolist()
top_keywords_2015 = tfidf_df.iloc[2].nlargest(10).index.tolist()

print("✅ 2013년 주요 키워드:", top_keywords_2013)
print("✅ 2014년 주요 키워드:", top_keywords_2014)
print("✅ 2015년 주요 키워드:", top_keywords_2015)



import matplotlib.pyplot as plt
import seaborn as sns

# 🔹 키워드 변화를 보기 위해 연도별 출현 빈도 비교
common_keywords = set(top_keywords_2013) | set(top_keywords_2014) | set(top_keywords_2015)
common_keywords = list(common_keywords)  # 전체 공통 키워드 리스트

# 🔹 키워드별 연도별 빈도수 추출
keyword_trends = {
    "Keyword": [],
    "Year": [],
    "TF-IDF": []
}

for keyword in common_keywords:
    for year, row in zip([2013, 2014, 2015], tfidf_df.iterrows()):
        keyword_trends["Keyword"].append(keyword)
        keyword_trends["Year"].append(year)
        keyword_trends["TF-IDF"].append(row[1][keyword] if keyword in row[1] else 0)

trend_df = pd.DataFrame(keyword_trends)

# 🔹 시각화 (키워드별 트렌드)
plt.figure(figsize=(12, 6))
sns.lineplot(data=trend_df, x="Year", y="TF-IDF", hue="Keyword", marker="o")
plt.title("정책 키워드 변화 추이")
plt.xlabel("연도")
plt.ylabel("TF-IDF 점수")
plt.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
plt.show()


from wordcloud import WordCloud

# 🔹 WordCloud 생성 함수
def generate_wordcloud(text, title):
    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/malgun.ttf", 
        background_color="white",
        width=800,
        height=400
    ).generate(text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=16)
    plt.show()

# 🔹 연설문별 WordCloud 출력
generate_wordcloud(cleaned_2013, "박근혜 대통령 취임사 (2013)")
generate_wordcloud(cleaned_2014, "박근혜 대통령 신년 연설문 (2014)")
generate_wordcloud(cleaned_2015, "박근혜 대통령 신년 연설문 (2015)")


# 🔹 연설문 불러오기 함수
def load_text(file_path):
    with open(file_path, "r", encoding="cp949") as f:
        text_data = f.read()
    return text_data

# 🔹 3개 연설문 불러오기
text_2013 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령취임사_2013.txt")
text_2014 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령신년연설문_2014_01_06.txt")
text_2015 = load_text("C:/Users/Admin/Desktop/JY/Python/20250311/project/박근혜대통령신년연설문_2015_01_12.txt")

# 🔹 연설문 합치기
combined_text = text_2013 + " " + text_2014 + " " + text_2015


import pymysql

# 🔹 MySQL에서 불용어 가져오기
def get_stopwords_from_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="jiyeoun1",
        database="speech_analysis",
        charset="utf8"
    )
    cursor = conn.cursor()

    cursor.execute("SELECT word FROM stopwords;")
    stopwords = {row[0] for row in cursor.fetchall()}  # set으로 저장

    conn.close()
    return stopwords

stopwords = get_stopwords_from_db()


from konlpy.tag import Okt
import re

okt = Okt()

# 🔹 텍스트 정제 함수
def clean_text(text):
    text = re.sub(r"[^가-힣\s]", "", text)  # 특수문자 제거
    words = okt.nouns(text)  # 명사 추출
    words = [word for word in words if word not in stopwords]  # 불용어 제거
    return " ".join(words)  # 띄어쓰기로 구분된 문자열 반환

# 🔹 병합된 연설문 전처리
cleaned_combined_text = clean_text(combined_text)


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

# 🔹 한글 폰트 설정
if platform.system() == 'Windows':
    font_path = "c:/Windows/Fonts/malgun.ttf"
elif platform.system() == 'Darwin':  # MacOS
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
else:
    font_path = None  # 리눅스 환경

# 🔹 WordCloud 생성
wordcloud = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=400
).generate(cleaned_combined_text)

# 🔹 WordCloud 출력
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("박근혜 대통령 연설문 통합 WordCloud", fontsize=16)
plt.show()



from sklearn.feature_extraction.text import TfidfVectorizer

# 🔹 TF-IDF 벡터화
vectorizer = TfidfVectorizer(max_features=50)  # 상위 50개 키워드 추출
tfidf_matrix = vectorizer.fit_transform([cleaned_2013, cleaned_2014, cleaned_2015])
tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out())

# 🔹 연도별 상위 TF-IDF 정책 키워드 추출
top_keywords_2013 = tfidf_df.iloc[0].nlargest(10).index.tolist()
top_keywords_2014 = tfidf_df.iloc[1].nlargest(10).index.tolist()
top_keywords_2015 = tfidf_df.iloc[2].nlargest(10).index.tolist()

print("✅ 2013년 주요 정책 키워드:", top_keywords_2013)
print("✅ 2014년 주요 정책 키워드:", top_keywords_2014)
print("✅ 2015년 주요 정책 키워드:", top_keywords_2015)


from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import platform

# 🔹 한글 폰트 설정
if platform.system() == 'Windows':
    font_path = "c:/Windows/Fonts/malgun.ttf"
elif platform.system() == 'Darwin':  # MacOS
    font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
else:
    font_path = None  # 리눅스 환경

# 🔹 WordCloud 생성 함수
def generate_wordcloud(words, title):
    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        width=600,
        height=400
    ).generate(" ".join(words))

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title, fontsize=14)

# 🔹 WordCloud 시각화 (3개 비교)
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
generate_wordcloud(top_keywords_2013, "2013년 정책 키워드")

plt.subplot(1, 3, 2)
generate_wordcloud(top_keywords_2014, "2014년 정책 키워드")

plt.subplot(1, 3, 3)
generate_wordcloud(top_keywords_2015, "2015년 정책 키워드")

plt.tight_layout()
plt.show()



























