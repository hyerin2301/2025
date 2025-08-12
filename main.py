import streamlit as st

# --- MBTI별 테마 색상, 아이콘, 이미지, 직업 데이터 ---
mbti_data = {
    "INTJ": {
        "color": "#6A5ACD",
        "icon": "🧠",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "jobs": ["전략 기획가", "데이터 분석가", "연구원", "정책 자문가", "AI 전문가", "금융 애널리스트"]
    },
    "INTP": {
        "color": "#6495ED",
        "icon": "🔍",
        "image": "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        "jobs": ["소프트웨어 개발자", "과학자", "시스템 분석가", "작가", "UX 디자이너", "게임 개발자"]
    },
    "ENTJ": {
        "color": "#FF6347",
        "icon": "💼",
        "image": "https://cdn-icons-png.flaticon.com/512/3135/3135680.png",
        "jobs": ["CEO", "경영 컨설턴트", "프로젝트 매니저", "변호사", "투자자", "기업 전략가"]
    },
    "ENTP": {
        "color": "#FFA500",
        "icon": "🚀",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "jobs": ["기업가", "마케터", "방송인", "기획자", "광고 제작자", "벤처 투자자"]
    },
    "INFJ": {
        "color": "#9370DB",
        "icon": "🌸",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
        "jobs": ["심리상담가", "작가", "인권운동가", "교사", "정신건강 전문가", "사회 혁신가"]
    },
    "INFP": {
        "color": "#FF69B4",
        "icon": "🎨",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616418.png",
        "jobs": ["예술가", "작곡가", "사회복지사", "작가", "아동문학가", "영상 제작자"]
    },
    "ENFJ": {
        "color": "#FFB6C1",
        "icon": "🤝",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616497.png",
        "jobs": ["리더십 코치", "홍보 담당자", "교사", "사회운동가", "교육 컨설턴트", "팀 빌더"]
    },
    "ENFP": {
        "color": "#FFD700",
        "icon": "✨",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "jobs": ["창업가", "방송 작가", "광고 기획자", "배우", "콘텐츠 크리에이터", "여행 작가"]
    },
    "ISTJ": {
        "color": "#2E8B57",
        "icon": "📊",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616414.png",
        "jobs": ["회계사", "엔지니어", "군인", "판사", "데이터 관리자", "품질 검사원"]
    },
    "ISFJ": {
        "color": "#20B2AA",
        "icon": "💖",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "jobs": ["간호사", "교사", "사회복지사", "행정직", "가정 상담사", "비영리단체 운영자"]
    },
    "ESTJ": {
        "color": "#DC143C",
        "icon": "🏆",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616429.png",
        "jobs": ["관리자", "군 장교", "부동산 개발자", "공무원", "프로젝트 디렉터", "운영 관리자"]
    },
    "ESFJ": {
        "color": "#FF4500",
        "icon": "🎉",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616410.png",
        "jobs": ["간호사", "홍보 담당자", "교사", "이벤트 플래너", "웨딩 플래너", "고객 서비스 매니저"]
    },
    "ISTP": {
        "color": "#008080",
        "icon": "🔧",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616497.png",
        "jobs": ["정비사", "파일럿", "경찰관", "탐정", "기계 엔지니어", "스포츠 코치"]
    },
    "ISFP": {
        "color": "#3CB371",
        "icon": "📷",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616408.png",
        "jobs": ["사진작가", "디자이너", "요리사", "음악가", "패션 스타일리스트", "플로리스트"]
    },
    "ESTP": {
        "color": "#FF8C00",
        "icon": "⚡",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616430.png",
        "jobs": ["영업사원", "운동선수", "기업가", "경찰관", "이벤트 매니저", "구조대원"]
    },
    "ESFP": {
        "color": "#FF1493",
        "icon": "🎭",
        "image": "https://cdn-icons-png.flaticon.com/512/616/616410.png",
        "jobs": ["배우", "이벤트 기획자", "가수", "강사", "댄서", "유튜버"]
    }
}

# --- Streamlit UI ---
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💡", layout="centered")

st.title("💡 MBTI 기반 직업 추천 앱")
st.write("당신의 MBTI를 선택하면, 어울리는 직업과 관련 이미지를 보여드립니다!")

# MBTI 선택
mbti = st.selectbox("MBTI를 선택하세요", list(mbti_data.keys()))

# 선택 시 테마 적용
if mbti:
    theme = mbti_data[mbti]

    st.markdown(
        f"<h2 style='color:{theme['color']}'>{theme['icon']} {mbti} 추천 직업</h2>",
        unsafe_allow_html=True
    )

    # 이미지 표시
    st.image(theme["image"], width=150)

    # 직업 목록
    st.markdown(f"<h4 style='color:{theme['color']}'>추천 직업 리스트</h4>", unsafe_allow_html=True)
    for job in theme["jobs"]:
        st.write(f"- {job}")

    st.markdown("---")
    st.caption("💡 이 추천은 참고용이며, 실제 진로 결정은 다양한 요소를 고려해야 합니다.")
    
