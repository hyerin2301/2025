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
st.se
