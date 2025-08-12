import streamlit as st

# --- MBTI별 데이터 ---
mbti_data = {
    "INTJ": {
        "color": "#6A5ACD",
        "emoji": "🧠",
        "gif": "https://media.giphy.com/media/QNFhOolVeCzPQ2Mx85/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
            "https://cdn-icons-png.flaticon.com/512/616/616408.png",
            "https://cdn-icons-png.flaticon.com/512/616/616420.png"
        ],
        "jobs": ["전략 기획가", "데이터 분석가", "연구원", "정책 자문가", "AI 전문가", "금융 애널리스트"]
    },
    "ENTP": {
        "color": "#FFA500",
        "emoji": "🚀",
        "gif": "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/616/616430.png",
            "https://cdn-icons-png.flaticon.com/512/616/616408.png",
            "https://cdn-icons-png.flaticon.com/512/616/616409.png"
        ],
        "jobs": ["기업가", "마케터", "방송인", "기획자", "광고 제작자", "벤처 투자자"]
    },
    "INFJ": {
        "color": "#9370DB",
        "emoji": "🌸",
        "gif": "https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/616/616430.png",
            "https://cdn-icons-png.flaticon.com/512/616/616497.png",
            "https://cdn-icons-png.flaticon.com/512/616/616413.png"
        ],
        "jobs": ["심리상담가", "작가", "인권운동가", "교사", "정신건강 전문가", "사회 혁신가"]
    },
    "ENFP": {
        "color": "#FFD700",
        "emoji": "✨",
        "gif": "https://media.giphy.com/media/26AHONQ79FdWZhAI0/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/616/616410.png",
            "https://cdn-icons-png.flaticon.com/512/616/616408.png",
            "https://cdn-icons-png.flaticon.com/512/616/616412.png"
        ],
        "jobs": ["창업가", "방송 작가", "광고 기획자", "배우", "콘텐츠 크리에이터", "여행 작가"]
    },
    "ISTP": {
        "color": "#008080",
        "emoji": "🔧",
        "gif": "https://media.giphy.com/media/3o6MbhJvH9F9hzoPpu/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/616/616497.png",
            "https://cdn-icons-png.flaticon.com/512/616/616414.png",
            "https://cdn-icons-png.flaticon.com/512/616/616415.png"
        ],
        "jobs": ["정비사", "파일럿", "경찰관", "탐정", "기계 엔지니어", "스포츠 코치"]
    },
    "ESFP": {
        "color": "#FF1493",
        "emoji": "🎭",
        "gif": "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
        "images": [
            "https://cdn-icons-png.flaticon.com/512/616/616410.png",
            "https://cdn-icons-png.flaticon.com/512/616/616418.png",
            "https://cdn-icons-png.flaticon.com/512/616/616407.png"
        ],
        "jobs": ["배우", "이벤트 기획자", "가수", "강사", "댄서", "유튜버"]
    }
}

# --- 페이지 설정 ---
st.set_page_config(page_title="MBTI 직업 추천", page_icon="💡", layout="centered")

# --- 앱 타이틀 ---
st.markdown(
    """
    <h1 style="text-align:center; color:#ff6600;">
        💡 MBTI 기반 직업 추천 앱
    </h1>
    <p style="text-align:center;">당신의 MBTI를 선택하면, 어울리는 직업과 멋진 GIF & 이미지를 보여드립니다!</p>
    """,
    unsafe_allow_html=True
)

# --- MBTI 선택 ---
mbti = st.selectbox("MBTI를 선택하세요", list(mbti_data.keys()))

# --- 결과 표시 ---
if mbti:
    theme = mbti_data[mbti]

    # MBTI 타이틀
    st.markdown(
        f"<h2 style='color:{theme['color']}'>{theme['emoji']} {mbti} 추천 직업</h2>",
        unsafe_allow_html=True
    )

    # GIF 표시
    st.image(theme["gif"], width=300)

    # 직업 리스트
    st.markdown(f"<h3 style='color:{theme['color']}'>추천 직업</h3>", unsafe_allow_html=True)
    for job in theme["jobs"]:
        st.write(f"- {job}")

    # 이미지 여러 장 표시
    st.markdown(f"<h3 style='color:{theme['color']}'>관련 이미지</h3>", unsafe_allow_html=True)
    cols = st.columns(len(theme["images"]))
    for idx, img_url in enumerate(theme["images"]):
        with cols[idx]:
            st.image(img_url, use_column_width=True)

    # 구분선 + 안내
    st.markdown("---")
    st.caption("💡 이 추천은 참고용이며, 실제 진로 결정은 다양한 요소를 고려해야 합니다.")
