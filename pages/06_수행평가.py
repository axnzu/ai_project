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
st.write("서울시 휴게음식점 인허가 데이터를 활용한 카페 창업 아이디어 추천")

uploaded_file = st.file_uploader(
    "서울시 휴게음식점 인허가 CSV 업로드",
    type=["csv"]
)

if uploaded_file is None:
    st.info("CSV 파일을 업로드해주세요.")
    st.stop()

# CSV 읽기
df = None

for enc in ["cp949", "utf-8-sig", "utf-8"]:
    try:
        df = pd.read_csv(uploaded_file, encoding=enc)
        break
    except Exception:
        pass

if df is None:
    st.error("CSV 파일을 읽을 수 없습니다.")
    st.stop()

# 주소 컬럼 찾기
address_col = None

for col in [
    "소재지전체주소",
    "도로명전체주소"
]:
    if col in df.columns:
        address_col = col
        break

if address_col is None:
    for col in df.columns:
        if "주소" in str(col):
            address_col = col
            break

if address_col is None:
    st.error("주소 컬럼을 찾을 수 없습니다.")
    st.write(df.columns.tolist())
    st.stop()

# 카페 데이터만 추출
cafe_df = df.copy()

if "업태구분명" in cafe_df.columns:
    cafe_df = cafe_df[
        cafe_df["업태구분명"]
        .astype(str)
        .str.contains("커피|카페", na=False)
    ]

if len(cafe_df) == 0:
    cafe_df = df.copy()

# 자치구 추출
def extract_gu(text):

    if pd.isna(text):
        return "기타"

    match = re.search(r"(\S+구)", str(text))

    if match:
        return match.group(1)

    return "기타"

cafe_df["자치구"] = cafe_df[address_col].apply(extract_gu)

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

# 실제 사업장명 분석
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
            .head(50)
            .index
            .tolist()
        )

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

st.header("창업 조건 입력")

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

    cafe_names = []

    while len(cafe_names) < 3:

        if len(popular_words) > 0:

            word = random.choice(
                popular_words[:20]
            )

            name = f"{word} 카페"

        else:

            name = random.choice([
                "모먼트 카페",
                "블룸 카페",
                "라온 카페",
                "하루 카페",
                "포레스트 카페"
            ])

        if name not in cafe_names:
            cafe_names.append(name)

    concept = {
        "디저트 카페":"다양한 디저트와 커피를 함께 즐기는 공간",
        "브런치 카페":"식사와 커피를 동시에 즐길 수 있는 공간",
        "감성 카페":"사진 촬영과 분위기를 중시하는 공간",
        "공부 카페":"집중하기 좋은 조용한 공간",
        "반려동물 카페":"반려동물과 함께 방문 가능한 공간",
        "루프탑 카페":"개방감 있는 전망 중심 공간",
        "포토존 카페":"SNS 인증샷 중심 공간",
        "책 카페":"독서와 휴식을 위한 공간",
        "가족 카페":"가족 단위 방문객 중심 공간",
        "건강 음료 카페":"건강한 음료와 디저트 중심 공간"
    }

    menu_dict = {
        "봄":["벚꽃라떼","딸기케이크","유자에이드"],
        "여름":["망고빙수","콜드브루","수박주스"],
        "가을":["고구마라떼","밤케이크","단호박타르트"],
        "겨울":["초코라떼","생강차","뱅쇼"]
    }

    st.header("🎉 추천 결과")

    st.subheader("🏷 추천 카페 이름")

    for n in cafe_names:
        st.write("•", n)

    st.subheader("📖 컨셉 설명")
    st.success(concept[theme])

    st.subheader("🎯 추천 타깃")
    st.write(customer)

    st.subheader("☕ 시그니처 메뉴")

    for menu in menu_dict[season]:
        st.write("✔", menu)

    st.subheader("🪑 인테리어 추천")

    st.write(
        """
- 따뜻한 간접조명
- 포토존 구성
- 편안한 좌석 배치
- 브랜드 컬러 통일
"""
    )

    st.subheader("📢 홍보 문구")

    st.info(
        f"{district}에서 만나는 특별한 {theme}!"
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
