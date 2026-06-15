import streamlit as st
import pandas as pd
import random

# 페이지 설정
st.set_page_config(page_title="강남구 카페 맞춤형 컨셉 추천 서비스", layout="centered")

# 7. 제공된 파일 활용 및 데이터 로드
@st.cache_data
def load_data():
    try:
        return pd.read_csv('서울시_강남구_카페_영업중.csv')
    except FileNotFoundError:
        st.error("아래 링크에서 다운로드한 '서울시_강남구_카페_영업중.csv' 파일을 스크립트와 동일한 폴더에 위치시켜 주세요.")
        return None

df = load_data()

st.title("☕ 강남구 카페 맞춤형 컨셉 추천 시스템")
st.write("제공된 강남구 카페 실데이터를 기반으로 나만의 카페 컨셉과 추천 매장을 제안해 드립니다.")
st.markdown("---")

if df is not None:
    # 2. 카페의 여러 가지 테마 중 가장 인기 있는 10개 테마 정의
    # (실제 업태구분명 외에 대중적으로 강남구 상권에서 가장 수요가 높은 10대 테마를 제시합니다.)
    themes = [
        "디저트/베이커리 카페", "에스프레소 바", "감성/인스타 핫플 카페", 
        "북/스터디 카페", "반려동물 동반 카페", "플랜테리어/식물 카페", 
        "로스터리 전문 카페", "전통/퓨전 떡카페", "키즈/가족 친화형 카페", "비건/친환경 카페"
    ]
    
    # [설문조사 단계 시작]
    st.subheader("📋 나만의 카페 설문조사")
    
    # 2 & 3. 테마 선택
    selected_theme = st.selectbox("🎯 1. 관심 있는 카페 테마를 선택해 주세요:", themes)
    
    # 3. 주요 고객층 선택
    target_audience = st.selectbox("👥 2. 타겟으로 삼을 주요 고객층을 선택해 주세요:", [
        "2030 트렌디한 MZ세대", "3040 직장인 및 비즈니스 고객", 
        "가족 단위 및 학부모/어린이", "대학생 및 카공족(공부/작업)", "반려동물을 키우는 반려인 가구"
    ])
    
    # 4. 상권 선택
    commercial_area = st.selectbox("📍 3. 희망하거나 관심 있는 강남구 상권을 선택해 주세요:", [
        "오피스 밀집 지역 (테헤란로/역삼/선릉)", "트렌디한 핫플레이스 (신사 가로수길/압구정 로데오)", 
        "고급 주거 및 상업지 (청담동/도곡동)", "대학가 및 학원가 인근 (대치동)"
    ])
    
    # 5. 계절 입력
    season = st.radio("🌸 4. 가장 집중하고 싶은 핵심 계절을 선택해 주세요:", [
        "봄 (화사하고 산뜻한 무드)", "여름 (시원하고 청량한 무드)", 
        "가을 (차분하고 고즈넉한 무드)", "겨울 (따뜻하고 아늑한 무드)"
    ])
    
    # 설문 완료 버튼
    if st.button("✨ 맞춤형 카페 결과 보기"):
        st.markdown("---")
        st.success("🎉 설문조사가 완료되었습니다! 입력하신 조건을 바탕으로 분석한 결과입니다.")
        
        # 7. 실제 데이터 기반으로 조건에 따른 기존 강남구 카페 매장 무작위 샘플링
        # (테마에 맞춰 떡카페나 키즈카페일 경우 가중치를 주어 샘플링)
        if "떡카페" in selected_theme:
            filtered_df = df[df['업태구분명'] == '떡카페']
        elif "키즈" in selected_theme:
            filtered_df = df[df['업태구분명'] == '키즈카페']
        else:
            filtered_df = df[df['업태구분명'] == '커피숍']
            
        if filtered_df.empty:
            filtered_df = df  # 예외 처리
            
        # 가상의 매칭 및 실제 존재하는 강남구 매장 예시 매칭
        sampled_cafes = filtered_df.sample(min(3, len(filtered_df)))['사업장명'].tolist()
        
        # 6. 결과 출력 (테마, 고객층, 상권, 계절을 고려한 동적 가이드 생성)
        st.header(f"🔍 추천 컨셉 리포트: [{selected_theme}]")
        
        # 컨셉 설명 및 가이드북
        st.subheader("💡 1. 벤치마킹 추천 카페 이름 (실제 강남구 영업 매장)")
        st.write("현재 강남구에서 성황리에 영업 중인 유사 업태의 매장들입니다. 방문하여 상권을 분석해 보세요!")
        for name in sampled_cafes:
            st.markdown(f"- 🏪 **{name}**")
            
        st.subheader("🎯 2. 공간 및 브랜딩 컨셉 설명")
        st.write(f"이 카페는 **{commercial_area}**에서 **{target_audience}**을 타겟으로 삼기에 최적화된 공간입니다. "
                 f"특히 **{season}**의 계절감을 인테리어 소품이나 조명, 패브릭을 통해 극대화하여 계절별로 찍고 싶은 포토존을 형성하는 것이 핵심입니다.")
        
        st.subheader("🍹 3. 시그니처 메뉴 제안")
        if "디저트" in selected_theme or "떡카페" in selected_theme:
            st.markdown("- **메인 메뉴:** 강남의 세련미를 담아 재해석한 무스 케이크 또는 수제 크림 떡 플레이터")
            st.markdown(f"- **시그니처 음료:** {season.split()[0]}의 감성을 담은 수제 크림 아인슈페너")
        elif "에스프레소" in selected_theme or "로스터리" in selected_theme:
            st.markdown("- **메인 메뉴:** 바삭한 식감의 정통 이탈리안 크로아상과 비스코티")
            st.markdown(f"- **시그니처 음료:** 자체 블렌딩 원두로 내린 에스프레소 쇼콜라 및 시즈널 브루잉 커피")
        else:
            st.markdown("- **메인 메뉴:** 남녀노소 부담 없이 즐길 수 있는 시즈널 유기농 베이커리")
            st.markdown(f"- **시그니처 음료:** 신선한 제철 과일을 활용한 에이드 및 허브 티 에디션")
            
        st.subheader("🖼️ 4. 인테리어 및 공간 연출 추천")
        st.write(f"**{target_audience}**의 발길을 잡기 위해, 전체적으로 모던하면서도 {season.split()[0]}에 어울리는 따뜻한/시원한 톤의 마감재를 추천합니다. "
                 f"인스타그래머블한 대형 거울 구역이나, 혼자서도 편하게 작업할 수 있는 콘센트 좌석 배치를 상권의 특성에 맞게 유연하게 조율하세요.")
                 
        st.subheader("📢 5. 추천 홍보 및 마케팅 문구")
        st.info(f"✨ *\"오직 {commercial_area}에서만 느낄 수 있는 도심 속 여유. 이번 {season.split()[0]}, 당신을 위한 특별한 [{selected_theme}] 공간으로 초대합니다.\"*")
