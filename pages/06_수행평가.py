```python
import streamlit as st
import pandas as pd
import random
import re

st.set_page_config(
    page_title="서울 카페 창업 컨설턴트",
    page_icon="☕",
    layout="wide"
)

st.title("☕ 서울 카페 창업 컨설턴트")
st.caption("서울시 휴게음식점 인허가 데이터를 활용한 창업 아이디어 추천")

# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():

    df = pd.read_csv(
        "서울시 휴게음식점 인허가 정보 (1).csv",
        encoding="cp949"
    )

    return df

df = load_data()

# -----------------------------
# 카페 데이터 추출
# -----------------------------
cafe_df = df[
    df["업태구분명"].astype(str).str.contains(
        "커피|카페",
        na=False
    )
].copy()

# -----------------------------
# 자치구 추출
# -----------------------------
def extract_gu(address):

    try:
        result = re.search(r"서울특별시\s+(\S+구)", str(address))

        if result:
            return result.group(1)

    except:
        pass

    return "기타"

cafe_df["자치구"] = cafe_df["지번주소"].apply(extract_gu)

# -----------------------------
# 실제 인기 카페 이름 단어 추출
# -----------------------------
words = []

for name in cafe_df["사업장명"].dropna():

    name = str(name)

    tokens = re.findall(r"[가-힣A-Za-z]{2,}", name)

    words.extend(tokens)

freq = pd.Series(words).value_counts()

popular_words = list(freq.head(100).index)

# -----------------------------
# 사용자 입력
# -----------------------------

themes = [
    "디저트 카페",
    "브런치 카페",
    "감성 카페",
    "공부 카페",
    "반려동물 카페",
    "포토존 카페",
    "루프탑 카페",
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

districts = sorted(
    cafe_df["자치구"].dropna().unique()
)

seasons = [
    "봄",
    "여름",
    "가을",
    "겨울"
]

st.header("창업 조건 입력")

theme = st.selectbox("카페 테마", themes)

customer = st.selectbox("주요 고객층", customers)

district = st.selectbox("창업 희망 자치구", districts)

season = st.selectbox("계절", seasons)

# -----------------------------
# 추천 버튼
# -----------------------------
if st.button("🚀 창업 아이디어 추천"):

    district_count = len(
        cafe_df[cafe_df["자치구"] == district]
    )

    active_count = len(
        cafe_df[
            (cafe_df["자치구"] == district)
            &
            (cafe_df["영업상태명"] == "영업")
        ]
    )

    # 경쟁도 계산
    if active_count > 1500:
        competition = "매우 높음"
        score = 60

    elif active_count > 700:
        competition = "높음"
        score = 75

    elif active_count > 300:
        competition = "보통"
        score = 85

    else:
        competition = "낮음"
        score = 95

    # 카페 이름 추천
    cafe_names = []

    while len(cafe_names) < 3:

        word = random.choice(popular_words[:50])

        name = f"{word} {random.choice(['카페','커피','라운지','하우스'])}"

        if name not in cafe_names:
            cafe_names.append(name)

    # 시즌 메뉴
    season_menu = {
        "봄":["벚꽃라떼","딸기케이크","유자에이드"],
        "여름":["망고빙수","수박주스","콜드브루"],
        "가을":["고구마라떼","밤케이크","단호박타르트"],
        "겨울":["초코라떼","뱅쇼","생강차"]
    }

    st.header("🎉 AI 추천 결과")

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("🏷 추천 카페 이름")

        for n in cafe_names:
            st.write("•", n)

        st.subheader("📖 추천 컨셉")

        st.success(
            f"{theme} 컨셉을 중심으로 "
            f"{customer} 고객이 자주 찾는 공간을 목표로 운영"
        )

        st.subheader("☕ 시그니처 메뉴")

        for m in season_menu[season]:
            st.write("✔", m)

    with col2:

        st.subheader("📊 상권 분석")

        st.metric(
            "해당 자치구 카페 수",
            f"{district_count:,}"
        )

        st.metric(
            "영업중 카페 수",
            f"{active_count:,}"
        )

        st.metric(
            "창업 추천 점수",
            f"{score}점"
        )

        st.write(f"경쟁도 : {competition}")

    st.divider()

    st.subheader("🪑 인테리어 추천")

    st.write(
        """
        - SNS 인증샷 포토존
        - 따뜻한 간접조명
        - 편안한 좌석 배치
        - 브랜드 컬러 통일
        """
    )

    st.subheader("📢 홍보 문구")

    st.info(
        f"{district}에서 가장 특별한 {theme}, "
        f"지금 만나보세요."
    )

    st.subheader("📱 추천 해시태그")

    st.write(
        "#카페창업 #서울카페 #감성카페 "
        "#카페추천 #신상카페"
    )

    st.subheader("🚀 차별화 전략")

    st.write("""
    ✅ 시즌 한정 메뉴 출시
    ✅ SNS 인증 이벤트
    ✅ 스탬프 적립 제도
    ✅ 지역 커뮤니티 연계 행사
    """)

    st.subheader("💡 데이터 기반 인사이트")

    st.success(
        f"{district}에는 현재 "
        f"{active_count:,}개의 영업 중 카페가 있습니다. "
        f"차별화된 컨셉이 중요합니다."
    )
```
