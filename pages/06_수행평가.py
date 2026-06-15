```python
import streamlit as st
import pandas as pd
import random
import re

# ----------------------------------
# 페이지 설정
# ----------------------------------
st.set_page_config(
    page_title="AI 카페 창업 컨설턴트",
    page_icon="☕",
    layout="wide"
)

st.title("☕ AI 카페 창업 컨설턴트")
st.write("서울시 휴게음식점 인허가 데이터를 활용하여 카페 창업 아이디어를 추천합니다.")

# ----------------------------------
# CSV 업로드
# ----------------------------------
uploaded_file = st.file_uploader(
    "서울시 휴게음식점 인허가 CSV 파일 업로드",
    type=["csv"]
)

if uploaded_file is None:
    st.info("CSV 파일을 업로드해주세요.")
    st.stop()

# ----------------------------------
# 데이터 읽기
# ----------------------------------
try:
    df = pd.read_csv(uploaded_file, encoding="cp949")
except:
    try:
        df = pd.read_csv(uploaded_file, encoding="utf-8-sig")
    except:
        df = pd.read_csv(uploaded_file)

# ----------------------------------
# 주소 컬럼 찾기
# ----------------------------------
address_col = None

for col in df.columns:
    if "주소" in col:
        address_col = col
        break

if address_col is None:
    st.error("주소 관련 컬럼을 찾을 수 없습니다.")
    st.stop()

# ----------------------------------
# 자치구 추출
# ----------------------------------
def extract_gu(text):

    if pd.isna(text):
        return "기타"

    match = re.search(r"(\S+구)", str(text))

    if match:
        return match.group(1)

    return "기타"

df["자치구"] = df[address_col].apply(extract_gu)

district_counts = (
    df["자치구"]
    .value_counts()
    .sort_values(ascending=False)
)

districts = sorted(df["자치구"].unique())

# ----------------------------------
# 입력 항목
# ----------------------------------
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

st.header("📋 창업 조건 입력")

theme = st.selectbox("카페 테마", themes)

customer = st.selectbox("주요 고객층", customers)

district = st.selectbox("창업 희망 자치구", districts)

season = st.selectbox("계절", seasons)

# ----------------------------------
# 결과 생성
# ----------------------------------
if st.button("🚀 창업 아이디어 추천"):

    cafe_count = int(
        district_counts.get(district, 0)
    )

    if cafe_count > 3000:
        score = 60
        competition = "매우 높음"

    elif cafe_count > 1500:
        score = 75
        competition = "높음"

    elif cafe_count > 700:
        score = 85
        competition = "보통"

    else:
        score = 95
        competition = "낮음"

    first_words = [
        "모먼트",
        "블룸",
        "브리즈",
        "라온",
        "하루",
        "멜로우",
        "루미",
        "포레스트",
        "어반",
        "스테이"
    ]

    second_words = [
        "카페",
        "커피",
        "라운지",
        "하우스",
        "스토리"
    ]

    names = []

    while len(names) < 3:

        name = (
            random.choice(first_words)
            + " "
            + random.choice(second_words)
        )

        if name not in names:
            names.append(name)

    season_menus = {
        "봄": ["벚꽃라떼", "딸기케이크", "유자에이드"],
        "여름": ["망고빙수", "수박주스", "콜드브루"],
        "가을": ["고구마라떼", "밤케이크", "단호박타르트"],
        "겨울": ["초코라떼", "뱅쇼", "생강차"]
    }

    st.header("🎉 추천 결과")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏷 추천 카페 이름")

        for i, name in enumerate(names, start=1):
            st.write(f"{i}. {name}")

        st.subheader("📖 컨셉 설명")

        st.success(
            f"{customer} 고객을 중심으로 한 "
            f"{theme} 전문 카페"
        )

        st.subheader("☕ 시그니처 메뉴")

        for menu in season_menus[season]:
            st.write(f"✔ {menu}")

    with col2:

        st.subheader("📊 상권 분석")

        st.metric(
            "해당 자치구 업소 수",
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

    st.write("""
    • 따뜻한 조명 사용

    • SNS 포토존 설치

    • 편안한 좌석 배치

    • 브랜드 컬러 통일
    """)

    st.subheader("📢 홍보 문구")

    st.info(
        f"{district}에서 만나는 특별한 {theme}!"
    )

    st.subheader("📱 추천 해시태그")

    st.write(
        "#카페창업 #서울카페 #감성카페 #신상카페 #카페추천"
    )

    st.subheader("🚀 차별화 전략")

    st.write("✅ 시즌 한정 메뉴 운영")
    st.write("✅ SNS 인증 이벤트")
    st.write("✅ 스탬프 적립 프로그램")
    st.write("✅ 지역 커뮤니티 연계 행사")

# ----------------------------------
# 데이터 현황
# ----------------------------------
st.divider()

st.subheader("서울 자치구별 업소 수 TOP 10")

st.bar_chart(
    district_counts.head(10)
)
```
