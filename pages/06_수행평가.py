import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(
    page_title="AI 카페 창업 컨설턴트",
    page_icon="☕",
    layout="wide"
)

# =========================
# 데이터 불러오기
# =========================

@st.cache_data
def load_data():

    encodings = ["cp949", "utf-8", "utf-8-sig"]

    for enc in encodings:
        try:
            return pd.read_csv("cafe_data.csv", encoding=enc)
        except:
            pass

    return pd.read_csv("cafe_data.csv")

try:
    df = load_data()

except Exception as e:
    st.error(f"파일을 읽을 수 없습니다.\n{e}")
    st.stop()

# =========================
# 자치구 추출
# =========================

def extract_gu(text):

    if pd.isna(text):
        return "기타"

    match = re.search(r"(\S+구)", str(text))

    if match:
        return match.group(1)

    return "기타"

address_col = None

for col in df.columns:

    if "주소" in col:
        address_col = col
        break

if address_col is None:
    st.error("주소 컬럼을 찾을 수 없습니다.")
    st.stop()

df["자치구"] = df[address_col].apply(extract_gu)

# =========================
# 카페 수 분석
# =========================

district_counts = (
    df["자치구"]
    .value_counts()
    .sort_values(ascending=False)
)

districts = sorted(df["자치구"].unique())

# =========================
# UI
# =========================

st.title("☕ AI 카페 창업 컨설턴트")

st.write(
    "서울시 휴게음식점 인허가 데이터를 활용하여 "
    "카페 창업 아이디어를 추천합니다."
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

theme = st.selectbox(
    "카페 테마 선택",
    themes
)

customer = st.selectbox(
    "주요 고객층 선택",
    customers
)

district = st.selectbox(
    "창업 희망 자치구",
    districts
)

season = st.selectbox(
    "계절 선택",
    seasons
)

# =========================
# 결과 생성
# =========================

if st.button("🚀 창업 아이디어 추천"):

    cafe_count = int(
        district_counts.get(district, 0)
    )

    if cafe_count > 3000:
        competition = "매우 높음"
        score = 60

    elif cafe_count > 1500:
        competition = "높음"
        score = 75

    elif cafe_count > 700:
        competition = "보통"
        score = 85

    else:
        competition = "낮음"
        score = 95

    first_names = [
        "모먼트",
        "블룸",
        "브리즈",
        "라온",
        "포레스트",
        "루미",
        "하루",
        "멜로우",
        "스테이",
        "어반"
    ]

    second_names = [
        "카페",
        "커피",
        "라운지",
        "하우스",
        "스토리",
        "플레이스"
    ]

    names = []

    while len(names) < 3:

        name = (
            random.choice(first_names)
            + " "
            + random.choice(second_names)
        )

        if name not in names:
            names.append(name)

    season_menus = {
        "봄": ["벚꽃라떼", "딸기케이크", "유자에이드"],
        "여름": ["망고빙수", "콜드브루", "수박주스"],
        "가을": ["고구마라떼", "밤케이크", "단호박타르트"],
        "겨울": ["초코라떼", "뱅쇼", "생강차"]
    }

    st.header("🎉 추천 결과")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏷 추천 카페 이름")

        for idx, name in enumerate(names, start=1):
            st.write(f"{idx}. {name}")

        st.subheader("📖 컨셉 설명")

        st.success(
            f"{customer} 고객이 자주 방문하고 "
            f"오래 머물고 싶은 {theme} 컨셉"
        )

        st.subheader("☕ 시그니처 메뉴")

        for menu in season_menus[season]:
            st.write("✔", menu)

    with col2:

        st.subheader("📊 상권 분석")

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

        st.subheader("🪑 인테리어 추천")

        st.write(
            """
            • 따뜻한 간접조명

            • SNS 포토존 설치

            • 편안한 좌석 구성

            • 브랜드 컬러 통일
            """
        )

    st.divider()

    st.subheader("📢 홍보 문구")

    st.info(
        f"{district}에서 만나는 특별한 {theme}! "
        f"오늘의 여유를 즐겨보세요."
    )

    st.subheader("📱 추천 해시태그")

    st.write(
        "#카페추천 #감성카페 #서울카페 "
        "#신상카페 #커피맛집"
    )

    st.subheader("🚀 차별화 전략")

    st.write("✅ 시즌 한정 메뉴 운영")
    st.write("✅ SNS 인증 이벤트")
    st.write("✅ 스탬프 적립 제도")
    st.write("✅ 지역 커뮤니티 연계")

    st.subheader("💡 데이터 기반 인사이트")

    st.success(
        f"{district}에는 현재 약 {cafe_count:,}개의 "
        f"휴게음식점이 등록되어 있습니다."
    )

# =========================
# 자치구 현황
# =========================

st.divider()

st.subheader("서울 자치구별 휴게음식점 수 TOP 10")

st.bar_chart(
    district_counts.head(10)
)
