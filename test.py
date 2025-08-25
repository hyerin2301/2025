import streamlit as st
from datetime import datetime, date, time, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

# -----------------------------
# 배경 & 테마 (달+구름 있는 배경 이미지)
# -----------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: url('https://i.imgur.com/7d3Xb7Z.jpg') no-repeat center center fixed;
        background-size: cover;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .css-16idsys p {
        color: #F4F6FF !important;
        text-shadow: 0 1px 2px rgba(0,0,0,0.45);
    }
    .title {
        text-align:center; 
        font-size: 42px; 
        font-weight: 800; 
        color: #FFD369;
        text-shadow: 2px 2px 6px #000;
    }
    .subtitle {
        text-align:center; 
        color:#EAEAEA; 
        margin-top: -8px;
    }
    .pill {
        border-radius: 16px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 8px 22px rgba(0,0,0,0.35);
        background: rgba(0,0,0,0.55);
        color:white;
        text-align:center;
        backdrop-filter: blur(4px);
    }
    .badge {
        display:inline-block;
        padding: 4px 10px; 
        border-radius: 999px; 
        background:#FFD369; 
        color:#000; 
        font-weight:700; 
        margin-bottom:8px;
    }
    .time-big {
        font-size: 28px; 
        font-weight: 800; 
        color:#FFF;
        letter-spacing: 0.5px;
    }
    .tip {
        background: rgba(255,248,231,0.95);
        border: 1px dashed #FFD27D;
        padding: 12px 14px;
        border-radius: 12px;
        color:#7A5B00;
    }
    .float-emoji {
        display:flex; 
        justify-content:center; 
        gap:14px; 
        margin: 4px 0 10px;
    }
    .float-emoji img {
        width: 46px; height: 46px;
        filter: drop-shadow(0 2px 6px rgba(0,0,0,0.45));
        animation: bob 3.6s ease-in-out infinite;
    }
    .float-emoji img:nth-child(2){ animation-duration: 4.2s; }
    .float-emoji img:nth-child(3){ animation-duration: 3.2s; }
    @keyframes bob {
        0%   { transform: translateY(0px);   opacity: 0.95; }
        50%  { transform: translateY(-6px);  opacity: 1;    }
        100% { transform: translateY(0px);   opacity: 0.95; }
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 헤더
# -----------------------------
st.markdown("<div class='title'>🌙 개운하게 일어나려면 언제 자야 할까? ⏰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>수면 주기(약 90분)와 입면 시간을 반영해 권장 취침 시각을 안내합니다.</div>", unsafe_allow_html=True)

# 움직이는 이모지 (GIF)
st.markdown(
    """
    <div class="float-emoji">
        <img src="https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif">
        <img src="https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif">
        <img src="https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif">
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 입력 영역
# -----------------------------
st.markdown("### 💡 입력")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    wake_date = st.date_input("📅 기상 날짜 선택", date.today())
with col2:
    wake_time_only = st.time_input("⏰ 기상 시각 (5분 단위)", value=time(7, 0), step=300)
with col3:
    fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 60, 15, step=5)

cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1)

# -----------------------------
# 계산 함수
# -----------------------------
def compute_bedtimes(wake_date: date, wake_t: time, fall_min: int, cycle_len: int, cycles=(3,4,5,6)):
    base_wake = datetime.combine(wake_date, wake_t)
    results = []
    for n in cycles:
        total_min = fall_min + cycle_len * n
        bedtime = base_wake - timedelta(minutes=total_min)
        results.append((n, bedtime))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

results = compute_bedtimes(wake_date, wake_time_only, fall_asleep_min, cycle_min)

# -----------------------------
# 출력
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")
cards = st.columns(len(results))

emoji_gifs = [
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
]

WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]

for idx, (n, bt) in enumerate(results):
    label_date = f"{bt.month}월 {bt.day}일({WEEKDAY_KO[bt.weekday()]})"
    label_time = bt.strftime("%H:%M")
    wake_label = datetime.combine(wake_date, wake_time_only).strftime("%H:%M")

    with cards[idx]:
        st.markdown(
            f"""
            <div class="pill">
                <div class="badge">{n}주기 수면</div>
                <img src="{emoji_gifs[idx % len(emoji_gifs)]}" width="80"><br>
                <div class="time-big">🛏️ {label_time}</div>
                <div style="color:#ddd; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid rgba(255,255,255,0.2); margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {label_date} {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

best = sorted(results, key=lambda x: abs(x[0]-5))[0]
best_time = best[1].strftime("%H:%M")
st.markdown(
    f"""
    <div class="tip" style="margin-top:10px;">
        ✅ 추천: 일반적으로 4~5주기 (약 6~7.5시간 수면)이 무난합니다.  
        현재 설정에서는 {best[0]}주기 기준 {best[1].strftime("%m/%d")} {best_time} 취침이 좋아요!
    </div>
    """,
    unsafe_allow_html=True
)
