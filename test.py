import streamlit as st
from PIL import Image

# 🎵 기분별 음악 추천 데이터
music_data = {
    "행복 😊": {
        "desc": "기분이 좋아서 세상이 반짝거릴 때 어울리는 음악이에요!",
        "songs": [
            ("Pharrell Williams - Happy", "https://www.youtube.com/watch?v=ZbZSe6N_BXs"),
            ("BTS - Dynamite", "https://www.youtube.com/watch?v=gdZLi9oWNZg"),
            ("Red Velvet - Power Up", "https://www.youtube.com/watch?v=WyiIGEHQP8o"),
        ],
        "emoji": "✨🌈🎉",
        "bg": "https://images.unsplash.com/photo-1506784983877-45594efa4cbe"
    },
    "우울 😢": {
        "desc": "마음이 조금 무거울 때 위로가 되어줄 음악이에요.",
        "songs": [
            ("IU - 밤편지", "https://www.youtube.com/watch?v=BzYnNdJhZQw"),
            ("Sam Smith - Stay With Me", "https://www.youtube.com/watch?v=pB-5XG-DbAA"),
            ("Paul Kim - 모든 날, 모든 순간", "https://www.youtube.com/watch?v=0V0weuN1f8E"),
        ],
        "emoji": "🌧️💧🌙",
        "bg": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e"
    },
    "피곤 😴": {
        "desc": "지친 하루에 휴식을 주는 잔잔한 음악이에요.",
        "songs": [
            ("Lauv - I Like Me Better", "https://www.youtube.com/watch?v=BcqxLCWn-CE"),
            ("Crush - 잊어버리지마", "https://www.youtube.com/watch?v=_Eg9u6xM0lA"),
            ("Kina - Get You The Moon", "https://www.youtube.com/watch?v=FJt7gNi3Nr4"),
        ],
        "emoji": "😌☕🌙",
        "bg": "https://images.unsplash.com/photo-1501973801540-537f08ccae7b"
    },
    "설렘 💖": {
        "desc": "두근거리는 마음을 더 빛내줄 설레는 음악이에요.",
        "songs": [
            ("Bolbbalgan4 - 우주를 줄게", "https://www.youtube.com/watch?v=6fUZey6-bok"),
            ("Justin Bieber - Love Yourself", "https://www.youtube.com/watch?v=oyEuk8j8imI"),
            ("Day6 - You Were Beautiful", "https://www.youtube.com/watch?v=Rrh3sZg4Q1c"),
        ],
        "emoji": "💘🌸🌟",
        "bg": "https://images.unsplash.com/photo-1517841905240-472988babdf9"
    },
    "집중 🔥": {
        "desc": "공부나 작업에 몰입할 때 어울리는 음악이에요.",
        "songs": [
            ("Lo-fi hip hop beats", "https://www.youtube.com/watch?v=jfKfPfyJRdk"),
            ("Chillhop Essentials", "https://www.youtube.com/watch?v=7NOSDKb0HlU"),
            ("Classical Study Music", "https://www.youtube.com/watch?v=wp6ZG0MpXqY"),
        ],
        "emoji": "📚💡⚡",
        "bg": "https://images.unsplash.com/photo-1507842217343-583bb7270b66"
    }
}

# 🎨 페이지 설정
st.set_page_config(page_title="기분별 음악 추천 🎵", page_icon="🎶", layout="wide")

# 상단 제목
st.markdown("<h1 style='text-align: center; color: #ff4b4b;'>🎶 기분별 음악 추천 🎶</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>오늘의 기분에 맞는 노래를 골라보세요 💖</h3>", unsafe_allow_html=True)

# 기분 선택
mood = st.selectbox("👉 지금 기분을 선택하세요!", list(music_data.keys()))

# 배경 이미지
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{music_data[mood]['bg']}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# 설명 + 이모지
st.markdown(f"### {music_data[mood]['emoji']} {music_data[mood]['desc']}")

# 음악 리스트 출력
for title, url in music_data[mood]["songs"]:
    st.markdown(f"🎵 **{title}**")
    st.video(url)
    st.write("---")

