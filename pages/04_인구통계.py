import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# -----------------------------------
# 한글 폰트 설정 (Streamlit Cloud 대응)
# -----------------------------------
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["axes.unicode_minus"] = False

# -----------------------------------
# 데이터 불러오기
# -----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("population.csv", encoding="utf-8")
    return df

df = load_data()

st.title("서울시 연령별 인구 분석")

# -----------------------------------
# 행정구 선택
# -----------------------------------
districts = df["행정구역"].tolist()

selected_district = st.selectbox(
    "행정구를 선택하세요",
    districts
)

# -----------------------------------
# 선택된 행 추출
# -----------------------------------
selected_row = df[df["행정구역"] == selected_district].iloc[0]

# -----------------------------------
# 나이 컬럼 찾기
# -----------------------------------
age_columns = []

for col in df.columns:
    if "세" in col:
        age_columns.append(col)

# -----------------------------------
# 나이 / 인구 데이터 생성
# -----------------------------------
ages = []
population = []

for col in age_columns:

    age_text = (
        col.replace("세", "")
           .replace(" 이상", "")
           .strip()
    )

    try:
        age = int(age_text)

        value = selected_row[col]

        ages.append(age)
        population.append(value)

    except:
        continue

# -----------------------------------
# 그래프 생성
# -----------------------------------
fig, ax = plt.subplots(figsize=(15, 6))

ax.plot(
    ages,
    population,
    color="hotpink",
    linewidth=3
)

# 제목 및 축
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=20
)

ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# -----------------------------------
# 10살 단위 눈금 및 구분선
# -----------------------------------
ax.set_xticks(range(0, 101, 10))

ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

# -----------------------------------
# 그래프 스타일
# -----------------------------------
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 여백 자동 조정
plt.tight_layout()

# Streamlit 출력
st.pyplot(fig)
