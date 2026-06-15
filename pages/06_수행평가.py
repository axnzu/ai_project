import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(
    page_title="AI 카페 창업 컨설턴트",
    page_icon="☕",
    layout="wide"
)

st.title("☕ AI 카페 창업 컨설턴트")
st.caption("서울시 휴게음식점 인허가 데이터 기반")

# ==================================
# 데이터 로드
# ==================================
@st.cache_data
def load_data():

    for enc in ["cp949", "utf-8-sig", "utf-8"]:
        try:
            return pd.read_csv("cafe_data.csv", encoding=enc)
        except:
            pass

    return None


df = load_data()

if df is None:
    st.error("cafe_data.csv 파일을 찾을 수 없습니다.")
    st.stop()

# ==================================
# 카페 데이터만 추출
# ==================================
if "업태구분명" in df.columns:

    cafe_df = df[
        df["업태구분명"]
        .astype(str)
        .str.contains("커피|카페", na=False)
    ].copy()

else:
    cafe_df = df.copy()

# 카페가 하나도 안 잡히면 전체 사용
if len(cafe_df) == 0:
    cafe_df = df.copy()

# ==================================
# 자치구 추출
# ==================================
def extract_gu(address):

    if pd.isna(address):
        return "기타"

    match = re.search(r"(\S+구)", str(address))

    if match:
        return match.group(1)

    return "기타"


cafe_df["자치구"] = cafe_df["지번주소"].apply(extract_gu)

district_counts = (
    cafe_df["자치구"]
    .value_counts()
    .sort_values(ascending=False)
)

districts = sorted(
    cafe_df["자치구"]
    .dropna()
    .unique()
)

# ==================================
# 실제 사업장명 분석
# ==================================
popular_words = []

if "사업장명" in cafe_df.columns:

    words = []

    for name in cafe_df["사업장명"].dropna():

        tokens = re.findall(
            r"[가-힣A-Za-z]{2,}",
            str(name)
        )

        words.extend(tokens)

    if len(words) > 0:

        popular_words = (
            pd.Series(words)
            .value_counts()
            .head(100)
            .index
            .tolist()
        )

# ==================================
# 입력
# ==================================
themes = [
    "디저트 카페",
    "브런치 카페",
    "감성 카페",
    "공부 카페",
    "반려동물 카페",
    "루프탑 카페",
    "포토존 카페",
    "책 카페",
    "가족 카페",
    "건강 음료 카페"
]

customers = [
    "학생",
    "대학생",
    "직장인",
    "가족",
    "관광객",
    "중장년층"
]

seasons = [
    "봄",
    "여름",
    "가을",
    "겨울"
]

st.header("창업 조건 선택")

theme = st.selectbox(
    "카페 테마",
    themes
)

customer = st.selectbox(
    "주요 고객층",
    customers
)

district = st.selectbox(
    "창업 희망 자치구",
    districts
)

season = st.selectbox(
    "계절",
    seasons
)

# ==================================
# 추천 버튼
# ==================================
if st.button("🚀 창업 아이디어 추천"):

    cafe_count = int(
        district_counts.get(district, 0)
    )

    if cafe_count > 1500:
        competition = "매우 높음"
        score = 60

    elif cafe_count > 800:
        competition = "높음"
        score = 75

    elif cafe_count > 300:
        competition = "보통"
        score = 85

    else:
        competition = "낮음"
        score = 95

    # 실제 데이터 기반 이름 생성
    cafe_names = []

    while len(cafe_names) < 3:

        if len(popular_words) > 0:

            word = random.choice(
                popular_words[:30]
            )

            suffix = random.choice(
                ["카페", "커피", "라운지"]
            )

            name = f"{word} {suffix}"

        else:

            name = random.choice([
                "모먼트 카페",
                "블룸 카페",
                "하루 카페"
            ])

        if name not in cafe_names:
            cafe_names.append(name)

    concept_dict = {
        "디저트 카페":"다양한 디저트와 음료를 즐길 수 있는 공간",
        "브런치 카페":"식사와 커피를 함께 즐기는 공간",
        "감성 카페":"인테리어와 분위기를 강조한 공간",
        "공부 카페":"집중하기 좋은 조용한 공간",
        "반려동물 카페":"반려동물과 함께 이용하는 공간",
        "루프탑 카페":"전망과 휴식을 강조한 공간",
        "포토존 카페":"SNS 인증샷 중심 공간",
        "책 카페":"독서와 휴식을 위한 공간",
        "가족 카페":"가족 단위 방문객 중심 공간",
        "건강 음료 카페":"건강 음료 중심 공간"
    }

    season_menu = {
        "봄":["벚꽃라떼", "딸기케이크", "유자에이드"],
        "여름":["망고빙수", "수박주스", "콜드브루"],
        "가을":["고구마라떼", "밤케이크", "단호박타르트"],
        "겨울":["초코라떼", "생강차", "뱅쇼"]
    }

    st.header("🎉 창업 추천 결과")

    st.subheader("🏷 추천 카페 이름")

    for idx, name in enumerate(cafe_names, start=1):
        st.write(f"{idx}. {name}")

    st.subheader("📖 컨셉 설명")
    st.success(concept_dict[theme])

    st.subheader("☕ 시그니처 메뉴")

    for menu in season_menu[season]:
        st.write(f"✔ {menu}")

    st.subheader("🪑 인테리어 추천")

    st.write("""
- 따뜻한 간접조명
- SNS 포토존 설치
- 편안한 좌석 구성
- 우드톤 인테리어
- 계절 장식 활용
""")

    st.subheader("📢 홍보 문구")

    st.info(
        f"{district}에서 만나는 특별한 {theme}! "
        f"지금 방문해보세요."
    )

    st.subheader("📊 데이터 기반 상권 분석")

    st.metric(
        "해당 자치구 카페 수",
        f"{cafe_count:,}"
    )

    st.metric(
        "창업 추천 점수",
        f"{score}점"
    )

    st.metric(
        "경쟁도",
        competition
    )

st.divider()

st.subheader("서울 자치구별 카페 수 TOP 10")

st.bar_chart(
    district_counts.head(10)
)
