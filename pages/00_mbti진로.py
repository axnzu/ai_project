import streamlit as st

st.set_page_config(
    page_title="✨ MBTI 진로 추천기",
    page_icon="🚀",
    layout="centered"
)

# MBTI별 진로 데이터
mbti_jobs = {
    "INTJ": [
        {
            "job": "🧠 데이터 사이언티스트",
            "major": "컴퓨터공학과, 통계학과",
            "personality": "논리적이고 분석하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 6,500만 원"
        },
        {
            "job": "📈 전략 컨설턴트",
            "major": "경영학과, 경제학과",
            "personality": "큰 그림을 잘 보고 계획 세우는 스타일!",
            "salary": "평균 연봉 약 7,000만 원"
        }
    ],

    "INTP": [
        {
            "job": "💻 AI 개발자",
            "major": "인공지능학과, 소프트웨어학과",
            "personality": "호기심 많고 새로운 기술 좋아하는 타입!",
            "salary": "평균 연봉 약 6,800만 원"
        },
        {
            "job": "🔬 연구원",
            "major": "자연과학계열, 공학계열",
            "personality": "깊게 탐구하고 실험하는 걸 좋아하는 사람!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ENTJ": [
        {
            "job": "🏢 CEO / 창업가",
            "major": "경영학과, 창업학과",
            "personality": "리더십 있고 추진력이 강한 스타일!",
            "salary": "평균 연봉 약 8,000만 원 이상"
        },
        {
            "job": "📊 프로젝트 매니저",
            "major": "산업공학과, 경영학과",
            "personality": "사람들을 이끌고 목표 달성하는 걸 좋아함!",
            "salary": "평균 연봉 약 6,000만 원"
        }
    ],

    "ENTP": [
        {
            "job": "🎤 마케팅 기획자",
            "major": "광고홍보학과, 경영학과",
            "personality": "아이디어 많고 말하는 걸 좋아하는 타입!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🚀 스타트업 기획자",
            "major": "창업학과, 경영학과",
            "personality": "새로운 도전을 즐기는 사람!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "INFJ": [
        {
            "job": "🧡 상담심리사",
            "major": "심리학과, 상담학과",
            "personality": "공감 능력이 뛰어나고 사람 이야기를 잘 들어줌!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "✍️ 작가",
            "major": "문예창작과, 국어국문학과",
            "personality": "감수성이 풍부하고 상상력이 좋은 타입!",
            "salary": "평균 연봉 약 4,000만 원"
        }
    ],

    "INFP": [
        {
            "job": "🎨 일러스트레이터",
            "major": "디자인학과, 미술학과",
            "personality": "창의적이고 감성적인 사람!",
            "salary": "평균 연봉 약 4,200만 원"
        },
        {
            "job": "🎬 영상 크리에이터",
            "major": "영상학과, 미디어학과",
            "personality": "자기만의 개성을 표현하는 걸 좋아함!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ENFJ": [
        {
            "job": "👩‍🏫 교사",
            "major": "교육학과, 사범대",
            "personality": "사람들을 도와주고 이끄는 걸 좋아함!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🤝 HR 담당자",
            "major": "경영학과, 심리학과",
            "personality": "사람 관계를 잘 관리하는 타입!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ENFP": [
        {
            "job": "📱 콘텐츠 크리에이터",
            "major": "미디어학과, 방송연예과",
            "personality": "에너지 넘치고 표현력이 좋은 사람!",
            "salary": "평균 연봉 약 4,800만 원"
        },
        {
            "job": "🎉 이벤트 플래너",
            "major": "관광학과, 이벤트학과",
            "personality": "재밌는 아이디어가 넘치는 스타일!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ISTJ": [
        {
            "job": "🏦 회계사",
            "major": "회계학과, 경영학과",
            "personality": "꼼꼼하고 책임감 강한 타입!",
            "salary": "평균 연봉 약 7,000만 원"
        },
        {
            "job": "⚖️ 공무원",
            "major": "행정학과, 법학과",
            "personality": "안정적이고 체계적인 걸 좋아함!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "ISFJ": [
        {
            "job": "💉 간호사",
            "major": "간호학과",
            "personality": "배려심 많고 성실한 사람!",
            "salary": "평균 연봉 약 5,000만 원"
        },
        {
            "job": "🏥 물리치료사",
            "major": "물리치료학과",
            "personality": "사람을 도와주는 일에 보람을 느낌!",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ],

    "ESTJ": [
        {
            "job": "📋 경영 관리자",
            "major": "경영학과",
            "personality": "리더십 있고 현실적인 타입!",
            "salary": "평균 연봉 약 6,500만 원"
        },
        {
            "job": "👮 경찰관",
            "major": "경찰행정학과",
            "personality": "규칙을 중요하게 생각하고 책임감이 강함!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ESFJ": [
        {
            "job": "🩺 의료 코디네이터",
            "major": "보건행정학과",
            "personality": "친절하고 사람 챙기는 걸 좋아함!",
            "salary": "평균 연봉 약 4,500만 원"
        },
        {
            "job": "🏨 호텔리어",
            "major": "호텔관광학과",
            "personality": "사교적이고 서비스 정신이 뛰어남!",
            "salary": "평균 연봉 약 4,300만 원"
        }
    ],

    "ISTP": [
        {
            "job": "🔧 기계 엔지니어",
            "major": "기계공학과",
            "personality": "손으로 만드는 걸 좋아하는 실전형!",
            "salary": "평균 연봉 약 6,000만 원"
        },
        {
            "job": "🛠️ 자동차 정비사",
            "major": "자동차공학과",
            "personality": "문제 해결 능력이 뛰어난 타입!",
            "salary": "평균 연봉 약 4,500만 원"
        }
    ],

    "ISFP": [
        {
            "job": "🎵 작곡가",
            "major": "실용음악과",
            "personality": "감각적이고 예술적인 성향!",
            "salary": "평균 연봉 약 4,000만 원"
        },
        {
            "job": "🖌️ UX 디자이너",
            "major": "디자인학과",
            "personality": "예쁜 것과 편리한 걸 동시에 좋아함!",
            "salary": "평균 연봉 약 5,500만 원"
        }
    ],

    "ESTP": [
        {
            "job": "💼 영업 전문가",
            "major": "경영학과",
            "personality": "활발하고 사람 만나는 걸 좋아함!",
            "salary": "평균 연봉 약 5,500만 원"
        },
        {
            "job": "🎥 방송인",
            "major": "방송연예과",
            "personality": "무대 체질! 에너지 넘치는 타입!",
            "salary": "평균 연봉 약 5,000만 원"
        }
    ],

    "ESFP": [
        {
            "job": "🌟 연예인 / 배우",
            "major": "연극영화과",
            "personality": "끼 많고 주목받는 걸 좋아함!",
            "salary": "평균 연봉 약 5,000만 원 이상"
        },
        {
            "job": "✈️ 승무원",
            "major": "항공서비스학과",
            "personality": "친화력 좋고 밝은 에너지가 강점!",
            "salary": "평균 연봉 약 4,800만 원"
        }
    ]
}

st.title("✨ MBTI 진로 추천기 🚀")
st.write("나의 MBTI에 딱 맞는 진로를 알아보자! 😎")

mbti = st.selectbox(
    "🧩 너의 MBTI를 선택해줘!",
    list(mbti_jobs.keys())
)

if st.button("🔍 진로 추천 보기"):
    st.success(f"{mbti} 유형에게 어울리는 진로를 추천할게! 🎉")

    jobs = mbti_jobs[mbti]

    for idx, job in enumerate(jobs, start=1):
        st.markdown(f"---")
        st.subheader(f"{idx}. {job['job']}")

        st.write(f"📚 **추천 학과** : {job['major']}")
        st.write(f"💡 **잘 맞는 성격** : {job['personality']}")
        st.write(f"💰 **평균 연봉** : {job['salary']}")

    st.balloons()

st.markdown("---")
st.caption("🌈 재미로 보는 MBTI 진로 추천! 미래를 고민하는 데 참고해봐 😄")
