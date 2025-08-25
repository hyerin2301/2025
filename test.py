import streamlit as st
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo  # Python 3.9+

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

# -----------------------------
# 배경 & 테마 (외부 이미지 없이 동작하는 별밤 그라데이션)
# -----------------------------
st.markdown(
    """
    <style>
    /* 앱 전체 배경: 그라데이션 + 은은한 별 */
    [data-testid="stAppViewContainer"] {
        background: radial-gradient(1200px 600px at 20% 10%, #0b1536, #070B22 60%, #020511 100%);
        position: relative;
    }
    /* 반짝이는 별 오버레이 (CSS만으로 구현) */
    [data-testid="stAppViewContainer"]::before,
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(2px 2px at 20% 30%, rgba(255,255,255,0.6), rgba(255,255,255,0) 60%),
            radial-gradient(1.5px 1.5px at 70% 20%, rgba(255,255,255,0.5), rgba(255,255,255,0) 60%),
            radial-gradient(1.8px 1.8px at 40% 70%, rgba(255,255,255,0.45), rgba(255,255,255,0) 60%),
            radial-gradient(1.2px 1.2px at 85% 60%, rgba(255,255,255,0.55), rgba(255,255,255,0) 60%),
            radial-gradient(1.6px 1.6px at 10% 80%, rgba(255,255,255,0.35), rgba(255,255,255,0) 60%);
        animation: twinkle 6s infinite alternate;
    }
    [data-testid="stAppViewContainer"]::after {
        filter: blur(0.6px) brightness(0.9);
        animation-duration: 7.5s;
        opacity: 0.8;
    }
    @keyframes twinkle {
        0%   { opacity: 0.6; }
        100% { opacity: 1; }
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
# 한국(서울) 현재 시간 기준 앵커 날짜 설정
# 규칙:
#  - 현재 시간이 "오후(12시~23:59)"면 => 다음날 오전 기상 기준(예: 8/25 오후 → 8/26 오전 기준)
#  - 현재 시간이 "새벽(0시~03시)"면 => 오늘 오전 기상 기준(예: 8/26 01:00 → 8/26 오전 7시 등)
#  - 그 외(오전 03~11시)는 오늘 기준
# -----------------------------
KST = ZoneInfo("Asia/Seoul")
now = datetime.now(tz=KST)

def anchor_wake_date(now_dt: datetime) -> date:
    if now_dt.hour >= 12:
        return (now_dt + timedelta(days=1)).date()
    # 0~11시는 오늘 기준. (요청 예시: 26일 오전 1시 → 같은 날 오전 기상 기준)
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
        # 5분 단위 선택
        wake_time_only = st.time_input("기상 시각 (5분 단위)", value=time(7, 0), step=300,
                                       help="예: 오전 7시로 두고 계산하면, 권장 취침 시각이 카드로 표시됩니다.")
    with col2:
        fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 60, 15, step=5,
                                    help="평균 입면 시간. 카페인/스트레스가 있으면 늘려보세요.")
    with col3:
        cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1,
                              help="보통 90분 내외(개인차 존재). 85~95분 사이에서 조정 권장.")

    st.caption("🔁 권장 계산 주기: 3~6주기 (일반적으로 4~5주기가 무난합니다).")

# -----------------------------
# 계산 함수
# -----------------------------
def compute_bedtimes(wake_date: date, wake_t: time, fall_min: int, cycle_len: int, cycles=(3,4,5,6)):
    """
    wake_date: 기상 '날짜' (앵커)
    wake_t: 기상 '시각'
    """
    base_wake = datetime.combine(wake_date, wake_t)  # 앵커 날짜 적용
    results = []
    for n in cycles:
        total_min = fall_min + cycle_len * n
        bedtime = base_wake - timedelta(minutes=total_min)
        results.append((n, bedtime))
    # 늦게 자는 시간(최근 취침)이 위로 오도록 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    return results

cycles_to_show = (3,4,5,6)
results = compute_bedtimes(anchor_date, wake_time_only, fall_asleep_min, cycle_min, cycles_to_show)

# -----------------------------
# 출력 영역
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")

cards = st.columns(len(results))

# 움직이는 이모지 GIF들 (카드용)
emoji_gifs = [
    "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",  # 달 🌙
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",  # 별 ✨
    "https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif",  # 졸린 고양이 😴
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",  # 곰 🐻💤
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
                <div style="color:#ddd; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid rgba(255,255,255,0.2); margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {fmt_kor_date(anchor_date)} {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 베스트 추천 (5주기에 가장 가까운 값을 추천)
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
    - 스트레스/카페인 섭취 시 **입면 시간이 길어질 수 있어요** → 슬라이더로 조정해 보세요.  
    - 수면 주기는 개인차가 있으니 **85~95분 범위**에서 조정하며 본인 컨디션을 확인해 보세요.  
    - 주말에도 기상 시각을 크게 바꾸지 않으면 월요일 컨디션 유지에 도움이 됩니다 🌞  
    """
)
st.caption("⚠️ 본 도구는 일반적인 수면 주기 모델을 따른 참고용이며, 개인별 차이가 존재합니다.")
