import streamlit as st
from datetime import datetime, time, timedelta

# -----------------------------
# 기본 설정 & 스타일
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

# 배경 이미지 + 글자 색상
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-image: url("https://i.ibb.co/3CvZzPt/night-sky.jpg"); /* 밤하늘 배경 */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
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
        color:#EEE; 
        margin-top: -10px;
    }
    .pill {
        border-radius: 16px;
        padding: 14px 18px;
        margin: 8px 0;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 6px 18px rgba(0,0,0,0.3);
        background: rgba(0,0,0,0.6);
        color:white;
        text-align:center;
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
        background: rgba(255,248,231,0.9);
        border: 1px dashed #FFD27D;
        padding: 12px 14px;
        border-radius: 12px;
        color:#7A5B00;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 제목 & 부제목
# -----------------------------
st.markdown("<div class='title'>🌙 개운하게 일어나려면 언제 자야 할까? ⏰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>수면 주기(약 90분)와 입면 시간을 반영해 권장 취침 시각을 알려드려요.</div>", unsafe_allow_html=True)
st.markdown("")

# -----------------------------
# 입력 영역
# -----------------------------
with st.container():
    st.markdown("### 💡 입력")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        wake_time = st.time_input("기상 시각", value=time(7, 0), step=300, help="5분 단위 선택 가능")
    with col2:
        fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 40, 15, step=5, help="평균적으로 잠드는 데 걸리는 시간 (기본 15분)")
    with col3:
        cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1, help="보통 90분 전후, 개인차가 있어요.")

    st.caption("🔁 권장 계산 주기: 3~6주기 (4~5주기 권장) — 너무 과도한 수면은 오히려 컨디션을 해칠 수 있어요.")

# -----------------------------
# 계산 함수
# -----------------------------
def compute_bedtimes(wake_t: time, fall_min: int, cycle_len: int, cycles=(3,4,5,6)):
    base_date = datetime.combine(datetime.today().date(), wake_t)
    results = []
    for n in cycles:
        total_min = fall_min + cycle_len * n
        bedtime = base_date - timedelta(minutes=total_min)
        results.append((n, bedtime))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

cycles_to_show = (3,4,5,6)
results = compute_bedtimes(wake_time, fall_asleep_min, cycle_min, cycles_to_show)

# -----------------------------
# 출력 영역
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")

cards = st.columns(len(results))

# 움직이는 이모지 GIF들
emoji_gifs = [
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",  # 달 🌙
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",  # 별 ✨
    "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",  # 눈감는 고양이 😴
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",  # 곰 🐻💤
]

for idx, (n, bt) in enumerate(results):
    with cards[idx]:
        label_date = bt.strftime("%m/%d (%a)")
        label_time = bt.strftime("%H:%M")
        wake_label = datetime.combine(datetime.today().date(), wake_time).strftime("%H:%M")

        st.markdown(
            f"""
            <div class="pill">
                <div class="badge">{n}주기 수면</div>
                <img src="{emoji_gifs[idx % len(emoji_gifs)]}" width="80"><br>
                <div class="time-big">{label_time}</div>
                <div style="color:#ddd; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid rgba(255,255,255,0.2); margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 베스트 추천 설명
best = sorted(results, key=lambda x: abs(x[0]-5))[0]
best_time = best[1].strftime("%H:%M")
st.markdown(
    f"""
    <div class="tip" style="margin-top:10px;">
        ✅ <b>추천</b>: 보통 <b>4~5주기</b> (약 6~7.5시간 수면)이 가장 무난해요.  
        현재 설정에서는 <b>{best[0]}주기</b> 기준 <b>{best_time}</b> 취침이 좋아요!
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
    - 스트레스/카페인 섭취 시 **입면 시간이 길어질 수 있어요** → 슬라이더로 조정하세요.  
    - 수면 주기는 개인차가 있으니 **85~95분 범위**에서 조정해 보세요.  
    - 주말에도 기상 시각을 크게 바꾸지 않으면 월요일 컨디션이 좋아져요 🌞  
    """
)

st.caption("⚠️ 본 계산기는 일반적인 수면 주기 모델을 따른 참고용 도구이며, 개인별 차이가 존재합니다.")
