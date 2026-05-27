import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# -----------------------------------
# 한글 폰트 설정
# -----------------------------------
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------------
# 페이지 설정
# -----------------------------------
st.set_page_config(
    page_title="서울시 인구 분석",
    layout="wide"
)

st.title("서울시 연령별 인구 분석")

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("population.csv", encoding="cp949")
    except:
        df = pd.read_csv("population.csv", encoding="euc-kr")

    return df


df = load_data()

# -----------------------------------
# 행정구 선택
# -----------------------------------
districts = df["행정구역"].tolist()

selected_district = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# -----------------------------------
# 선택한 행 가져오기
# -----------------------------------
selected_row = df[df["행정구역"] == selected_district].iloc[0]

# -----------------------------------
# 2026년04월 연령 컬럼만 선택
# -----------------------------------
age_columns = []

for col in df.columns:

    if "2026년04월_거주자_" in col and "세" in col:

        # 총인구 제외
        if "총인구수" not in col and "연령구간인구수" not in col:
            age_columns.append(col)

# -----------------------------------
# 나이 / 인구수 추출
# -----------------------------------
ages = []
population = []

for col in age_columns:

    # 숫자 추출
    match = re.search(r'_(\d+)세', col)

    if match:

        age = int(match.group(1))

        value = str(selected_row[col]).replace(",", "")

        try:
            value = int(value)
        except:
            value = 0

        ages.append(age)
        population.append(value)

# -----------------------------------
# 데이터프레임 생성
# -----------------------------------
graph_df = pd.DataFrame({
    "age": ages,
    "population": population
})

graph_df = graph_df.sort_values("age")

# -----------------------------------
# 그래프 생성
# -----------------------------------
fig, ax = plt.subplots(figsize=(16, 7))

ax.plot(
    graph_df["age"],
    graph_df["population"],
    color="hotpink",
    linewidth=3
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=22
)

# 축
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# -----------------------------------
# 10살 단위 구분선
# -----------------------------------
ax.set_xticks(range(0, 101, 10))

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

# 스타일
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# -----------------------------------
# 출력
# -----------------------------------
st.pyplot(fig)
