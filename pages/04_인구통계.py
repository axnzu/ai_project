import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# 한글 폰트 설정
# -----------------------------
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="인구 통계",
    layout="wide"
)

st.title("행정구별 연령 인구 분석")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    try:
        df = pd.read_csv("population.csv", encoding="cp949")
    except:
        df = pd.read_csv("population.csv", encoding="euc-kr")

    return df

df = load_data()

# -----------------------------
# 컬럼 확인
# -----------------------------
st.write("현재 컬럼명:")
st.write(df.columns)

# -----------------------------
# 행정구 컬럼 자동 찾기
# -----------------------------
district_col = None

for col in df.columns:
    if "행정구역" in col:
        district_col = col
        break

if district_col is None:
    st.error("행정구역 컬럼을 찾을 수 없습니다.")
    st.stop()

# -----------------------------
# 행정구 선택
# -----------------------------
districts = df[district_col].unique()

selected_district = st.selectbox(
    "행정구 선택",
    districts
)

# -----------------------------
# 선택 데이터
# -----------------------------
selected_row = df[df[district_col] == selected_district].iloc[0]

# -----------------------------
# 나이 컬럼 찾기
# -----------------------------
age_columns = []

for col in df.columns:

    # 0세 ~ 100세 이상
    if "세" in str(col):

        # 총인구 같은 컬럼 제외
        if "계" not in str(col):
            age_columns.append(col)

# -----------------------------
# 데이터 생성
# -----------------------------
ages = []
population = []

for col in age_columns:

    try:
        age_text = (
            str(col)
            .split("세")[0]
            .replace(" ", "")
        )

        age = int(age_text)

        value = pd.to_numeric(selected_row[col], errors="coerce")

        ages.append(age)
        population.append(value)

    except:
        continue

# -----------------------------
# 데이터 정렬
# -----------------------------
data = pd.DataFrame({
    "age": ages,
    "population": population
})

data = data.sort_values("age")

# -----------------------------
# 그래프
# -----------------------------
fig, ax = plt.subplots(figsize=(16, 7))

ax.plot(
    data["age"],
    data["population"],
    color="hotpink",
    linewidth=3
)

# 제목
ax.set_title(
    f"{selected_district} 연령별 인구수",
    fontsize=20
)

# 축 이름
ax.set_xlabel("나이", fontsize=14)
ax.set_ylabel("인구수", fontsize=14)

# 10살 단위
ax.set_xticks(range(0, 101, 10))

# 세로선
ax.grid(
    axis="x",
    linestyle="--",
    alpha=0.5
)

# 스타일
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# -----------------------------
# 출력
# -----------------------------
st.pyplot(fig)
