import streamlit as st

# 페이지 설정
st.set_page_config(page_title="기분별 음악 추천 🎶", page_icon="🎧", layout="wide")

# 헤더
st.markdown(
    """
    <h1 style="text-align: center; color: #FF66B2;">
        🎶 기분별 음악 추천 🎶
    </h1>
    <p style="text-align: center; font-size:20px;">
        오늘 기분에 딱 맞는 음악을 들어보세요! 😊
    </p>
    """,
    unsafe_allow_html=True
)

# 기분 선택
mood = st.selectbox(
    "👉 지금 기분을 선택하세요:",
    ["행복 😊", "우울 😢", "피곤 😴", "설렘 💖", "집중 🔥"]
)

# 기분별 유튜브 링크 (모두 정상 재생 가능)
music_dict = {
    "행복 😊": [
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # 싸이 - 강남스타일
        "https://www.youtube.com/watch?v=OPf0YbXqDm0"   # Mark Ronson - Uptown Funk
    ],
    "우울 😢": [
        "https://www.youtube.com/watch?v=hLQl3WQQoQ0",  # Adele - Someone Like You
        "https://www.youtube.com/watch?v=RB-RcX5DS5A"   # Billie Eilish - lovely
    ],
    "피곤 😴": [
        "https://www.youtube.com/watch?v=ScMzIvxBSi4",  # Lofi Hip Hop
        "https://www.youtube.com/watch?v=2Vv-BfVoq4g"   # Ed Sheeran - Perfect
    ],
    "설렘 💖": [
        "https://www.youtube.com/watch?v=fRh_vgS2dFE",  # Justin Bieber - Sorry
        "https://www.youtube.com/watch?v=3AtDnEC4zak"   # Charlie Puth - We Don’t Talk Anymore
    ],
    "집중 🔥": [
        "https://www.youtube.com/watch?v=5qap5aO4i9A",  # Lofi Hip Hop Live
        "https://www.youtube.com/watch?v=jfKfPfyJRdk"   # Lofi Hip Hop Beats
    ]
}

# 선택된 기분의 음악 가져오기
videos = music_dict[mood]

st.write(f"### 🎧 {mood} 에 어울리는 음악 추천")

# 영상 출력
for link in videos:
    video_id = None
    if "v=" in link:
        video_id = link.split("v=")[-1]

    if video_id:
        st.markdown(
            f"""
            <iframe width="560" height="315" 
            src="https://www.youtube.com/embed/{video_id}" 
            frameborder="0" allow="accelerometer; autoplay; 
            clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen></iframe>
            """,
            unsafe_allow_html=True
        )


