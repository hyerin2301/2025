import streamlit as st
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

# -----------------------------
# 배경 & 테마 (깔끔한 연한 회색)
# -----------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f0f4f8;
        color: #222;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .css-16idsys p {
        color: #222 !important;
    }
    .title {
        text-align:center; 
        font-size: 42px; 
        font-weight: 800; 
        color: #1f2937;
    }
    .subtitle {
        text-align:center; 
        color:#4b5563; 
        margin-top: -8px;
    }
    .pill {
        border-radius: 16px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid rgba(0,0,0,0.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        background: #ffffff;
        color:#1f2937;
        text-align:center;
    }
    .badge {
        display:inline-block;
        padding: 4px 10px; 
        border-radius: 999px; 
        background:#3b82f6; 
        color:white; 
        font-weight:700; 
        margin-bottom:8px;
    }
    .time-big {
        font-size: 28px; 
        font-weight: 800; 
        color:#1f2937;
        letter-spacing: 0.5px;
    }
    .tip {
        background: #e0f2fe;
        border: 1px dashed #3b82f6;
        padding: 12px 14px;
        border-radius: 12px;
        color:#1e3a8a;
    }
    .float-emoji {
        display:flex; 
        justify-content:center; 
        gap:14px; 
        margin: 4px 0 10px;
    }
    .float-emoji img {
        width: 46px; height: 46px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
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
# 한국(서울) 현재 시간 기준 앵커 날짜 설정
# -----------------------------
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(tz=KST)

def anchor_wake_date(now_dt: datetime) -> date:
    if now_dt.hour >= 12:
        return (now_dt + timedelta(days=1)).date()
    return now_dt.date()

anchor_date = anchor_wake_date(now)

# 요일 한글
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]
def fmt_kor_date(d: date) -> str:
    return f"{d.month}월 {d.day}일({WEEKDAY_KO[d.weekday()]})"

# -----------------------------
# 헤더
# -----------------------------
st.markdown("<div class='title'>🌙 개운하게 일어나려면 언제 자야 할까? ⏰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>수면 주기(약 90분)와 입면 시간을 반영해 권장 취침 시각을 안내합니다.</div>", unsafe_allow_html=True)

# 움직이는 이모지
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

st.markdown(
    f"🗓️ <b>기준 날짜:</b> <code>{fmt_kor_date(anchor_date)}</code> 오전 기상 기준으로 계산합니다.",
    unsafe_allow_html=True
)

st.markdown("---")

# -----------------------------
# 입력 영역
# -----------------------------
with st.container():
    st.markdown("### 💡 입력")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        wake_time_only = st.time_input("기상 시각 (5분 단위)", value=time(7, 0), step=300)
    with col2:
        fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 60, 15, step=5)
    with col3:
        cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1)
    st.caption("🔁 권장 계산 주기: 3~6주기 (일반적으로 4~5주기가 무난합니다).")

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

cycles_to_show = (3,4,5,6)
results = compute_bedtimes(anchor_date, wake_time_only, fall_asleep_min, cycle_min, cycles_to_show)

# -----------------------------
# 출력 영역
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")
cards = st.columns(len(results))

emoji_gifs = [
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
]

for idx, (n, bt) in enumerate(results):
    label_date = f"{bt.month}월 {bt.day}일({WEEKDAY_KO[bt.weekday()]})"
    label_time = bt.strftime("%H:%M")
    wake_label = datetime.combine(anchor_date, wake_time_only).strftime("%H:%M")

    with cards[idx]:
        st.markdown(
            f"""
            <div class="pill">
                <div class="badge">{n}주기 수면</div>
                <img src="{emoji_gifs[idx % len(emoji_gifs)]}" width="80"><br>
                <div class="time-big">🛏️ {label_time}</div>
                <div style="color:#4b5563; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid rgba(0,0,0,0.1); margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {fmt_kor_date(anchor_date)} {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

best = sorted(results, key=lambda x: abs(x[0]-5))[0]
best_time = best[1].strftime("%H:%M")
st.markdown(
    f"""
    <div class="tip" style="margin-top:10px;">
        ✅ <b>추천</b>: 일반적으로 <b>4~5주기</b> (약 6~7.5시간 수면)이 무난합니다.  
        현재 설정에서는 <b>{best[0]}주기</b> 기준 <b>{fmt_kor_date(best[1].date())} {best_time}</b> 취침이 좋아요!
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 안내 & 팁
# -----------------------------
st.markdown("### 📝 사용 팁")
st.markdown(
    """
    - 스트레스/카페인 섭취 시 **입면 시간이 길어질 수 있어요** → 슬라이

