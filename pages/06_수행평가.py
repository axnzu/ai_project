import streamlit as st
import random

st.set_page_config(
    page_title="AI 카페 창업 컨설턴트",
    page_icon="☕",
    layout="wide"
)

st.title("☕ AI 카페 창업 컨설턴트")
st.markdown("테마, 고객층, 상권, 계절을 선택하면 맞춤형 카페 창업 아이디어를 추천해드립니다.")

# =====================
# 선택 항목
# =====================

themes = [
    "디저트 카페",
    "브런치 카페",
    "공부하기 좋은 카페",
    "반려동물 카페",
    "책 읽는 카페",
    "감성 카페",
    "루프탑 카페",
    "가족 카페",
    "포토존 카페",
    "건강 음료 카페"
]

customers = [
    "중고등학생",
    "대학생",
    "20~30대 직장인",
    "30~40대 직장인",
    "가족 단위 고객",
    "중장년층",
    "관광객"
]

markets = [
    "대학가",
    "오피스 상권",
    "주거 지역",
    "관광지",
    "번화가",
    "역세권"
]

seasons = [
    "봄",
    "여름",
    "가을",
    "겨울"
]

# =====================
# 데이터
# =====================

theme_data = {

    "디저트 카페": {
        "concept": "달콤한 디저트와 감성적인 공간을 중심으로 운영하는 카페",
        "menus": ["수제 티라미수", "딸기 케이크", "바닐라 콜드브루"],
        "interior": "파스텔톤 인테리어와 따뜻한 조명"
    },

    "브런치 카페": {
        "concept": "커피와 브런치를 함께 즐길 수 있는 라이프스타일 공간",
        "menus": ["에그 베네딕트", "프렌치 토스트", "아메리카노"],
        "interior": "우드톤 테이블과 넓은 창문"
    },

    "공부하기 좋은 카페": {
        "concept": "집중력 향상을 위한 조용한 학습 공간",
        "menus": ["콜드브루", "녹차라떼", "크로플"],
        "interior": "개인석과 콘센트가 많은 구조"
    },

    "반려동물 카페": {
        "concept": "반려동물과 함께 편안하게 머무를 수 있는 공간",
        "menus": ["수제 쿠키", "라떼", "과일 에이드"],
        "interior": "반려동물 놀이 공간 구성"
    },

    "책 읽는 카페": {
        "concept": "독서와 휴식을 동시에 즐길 수 있는 공간",
        "menus": ["드립커피", "치즈케이크", "허브티"],
        "interior": "대형 책장과 편안한 소파"
    },

    "감성 카페": {
        "concept": "SNS 감성을 자극하는 분위기 중심 카페",
        "menus": ["크림라떼", "수제 케이크", "말차라떼"],
        "interior": "은은한 조명과 감성 소품"
    },

    "루프탑 카페": {
        "concept": "전망과 분위기를 즐기는 공간",
        "menus": ["자몽에이드", "콜드브루", "브라우니"],
        "interior": "야외 테라스와 야간 조명"
    },

    "가족 카페": {
        "concept": "아이와 부모가 함께 즐길 수 있는 공간",
        "menus": ["와플", "핫초코", "과일주스"],
        "interior": "넓은 좌석과 키즈존"
    },

    "포토존 카페": {
        "concept": "인생샷 촬영이 가능한 트렌디 공간",
        "menus": ["레인보우 케이크", "크림소다", "딸기라떼"],
        "interior": "대형 포토존과 감각적 소품"
    },

    "건강 음료 카페": {
        "concept": "건강한 식재료를 활용한 웰빙 카페",
        "menus": ["ABC주스", "단백질 스무디", "그릭요거트"],
        "interior": "친환경 우드 인테리어"
    }

}

name_first = [
    "모먼트",
    "블룸",
    "브리즈",
    "하루",
    "오브",
    "포레스트",
    "멜로우",
    "라온",
    "스테이",
    "루미"
]

name_second = [
    "카페",
    "커피",
    "라운지",
    "하우스",
    "스토리",
    "가든",
    "테이블",
    "플레이스"
]

hashtags = [
    "#카페추천",
    "#감성카페",
    "#카페투어",
    "#데이트코스",
    "#핫플레이스",
    "#커피맛집",
    "#디저트맛집",
    "#주말나들이"
]

strategies = [
    "SNS 인증 이벤트 운영",
    "시즌 한정 메뉴 출시",
    "멤버십 적립 제도 운영",
    "포토존 마케팅 강화",
    "지역 커뮤니티 행사 개최",
    "리뷰 작성 고객 할인 이벤트"
]

success_points = [
    "고객층과 컨셉의 적합성이 높음",
    "SNS 확산 가능성이 높음",
    "재방문 고객 확보 가능",
    "차별화된 메뉴 운영 가능",
    "계절별 이벤트 활용 가능",
    "브랜드화 가능성이 높음"
]

season_special = {
    "봄": "벚꽃 시즌 한정 음료 출시",
    "여름": "빙수 및 아이스 음료 강화",
    "가을": "고구마·밤 디저트 출시",
    "겨울": "따뜻한 시즌 음료 출시"
}

# =====================
# 입력
# =====================

st.header("📋 창업 조건 입력")

theme = st.selectbox("카페 테마", themes)

customer = st.selectbox("주요 고객층", customers)

market = st.selectbox("상권", markets)

season = st.selectbox("계절", seasons)

# =====================
# 결과 생성
# =====================

if st.button("🚀 추천 결과 보기"):

    data = theme_data[theme]

    names = []
    while len(names) < 3:
        name = f"{random.choice(name_first)} {random.choice(name_second)}"
        if name not in names:
            names.append(name)

    st.header("🎉 AI 추천 결과")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏷️ 추천 카페 이름")

        for idx, name in enumerate(names, start=1):
            st.write(f"{idx}. {name}")

        st.subheader("📖 컨셉 설명")
        st.success(data["concept"])

        st.subheader("☕ 시그니처 메뉴")

        for menu in data["menus"]:
            st.write(f"✔ {menu}")

        st.subheader("📢 홍보 문구")

        slogan = f"{customer}들이 다시 찾고 싶은 {theme}, 지금 경험해보세요!"
        st.info(slogan)

    with col2:

        st.subheader("🪑 인테리어 추천")
        st.write(data["interior"])

        st.subheader("⭐ 예상 인기 메뉴")

        for menu in random.sample(data["menus"], len(data["menus"])):
            st.write(f"🔥 {menu}")

        st.subheader("📱 추천 해시태그")
        st.write(" ".join(random.sample(hashtags, 4)))

    st.divider()

    st.subheader("🚀 차별화 전략")

    for item in random.sample(strategies, 4):
        st.write(f"✅ {item}")

    st.subheader("📈 창업 성공 포인트")

    for point in random.sample(success_points, 4):
        st.write(f"✔ {point}")

    st.subheader("🌟 계절 마케팅 아이디어")

    st.success(season_special[season])

    st.subheader("💡 운영 팁")

    st.write(
        """
        - SNS 리뷰 이벤트를 적극 활용하세요.
        - 시그니처 메뉴를 대표 브랜드로 육성하세요.
        - 시즌별 신메뉴를 꾸준히 출시하세요.
        - 고객 사진 촬영 공간을 마련하면 홍보 효과가 커집니다.
        """
    )
