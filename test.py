import streamlit as st
from datetime import datetime, date, time, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

# -----------------------------
# 배경 & 테마 (깔끔한 색)
# -----------------------------
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
        color: #333;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .css-16idsys p {
        color: #333 !important;
    }
    .title {
        text-align:center; 
        font-size: 42px; 
        font-weight: 800; 
        color: #0d47a1;
    }
    .subtitle {
        text-align:center; 
        color:#0d47a1; 
        margin-top: -8px;
    }
    .pill {
        border-radius: 16px;
        padding: 14px 18px;
        margin: 10px 0;
        border: 1px solid rgba(0,0,0,0.18);
        box-shadow: 0 8px 22px rgba(0,0,0,0.15);
        background: rgba(255,255,255,0.85);
        color:#333;
        text-align:center;
    }
    .badge {
        display:inline-block;
        padding: 4px 10px; 
        border-radius: 999px; 
        background:#1976d2; 
        color:#fff; 
        font-weight:700; 
        margin-bottom:8px;
    }
    .time-big {
        font-size: 28px; 
        font-weight: 800; 
        color:#0d47a1;
        letter-spacing: 0.5px;
    }
    .tip {
        background: rgba(255,250,250,0.9);
        border: 1px dashed #1976d2;
        padding: 12px 14px;
        border-radius: 12px;
        color:#0d47a1;
    }
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 요일 한글
# -----------------------------
WEEKDAY_KO = ["월", "화", "수", "목", "금", "토", "일"]
def fmt_kor_date(d: date) -> str:
    return f"{d.month}월 {d.day}일({WEEKDAY_KO[d.weekday()]})"

# -----------------------------
# 헤더
# -----------------------------
st.markdown("<div class='title'>🌙 개운하게 일어나려면 언제 자야 할까? ⏰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>수면 주기(약 90분)와 입면 시간을 반영해 권장 취침 시각을 안내합니다.</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# 입력 영역
# -----------------------------
st.markdown("### 💡 입력")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    wake_date = st.date_input("기상할 날짜", value=date.today(), help="예: 2025-08-26")
with col2:
    wake_time_only = st.time_input("기상 시각 (5분 단위)", value=time(7, 0), step=300)
with col3:
    fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 60, 15, step=5)

cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1, help="보통 90분 내외(개인차 존재)")

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
results = compute_bedtimes(wake_date, wake_time_only, fall_asleep_min, cycle_min, cycles_to_show)

# -----------------------------
# 출력 영역
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")
cards = st.columns(len(results))

for idx, (n, bt) in enumerate(results):
    label_date = fmt_kor_date(bt.date())
    label_time = bt.strftime("%H:%M")
    wake_label = wake_time_only.strftime("%H:%M")
    with cards[idx]:
        st.markdown(
            f"""
            <div class="pill">
                <div class="badge">{n}주기 수면</div>
                <div class="time-big">🛏️ {label_time}</div>
                <div style="color:#555; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid rgba(0,0,0,0.1); margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {label_date} {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# 베스트 추천
# -----------------------------
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
    """,
    unsafe_allow_html=True
)
st.caption("⚠️ 본 도구는 일반적인 수면 주기 모델을 따른 참고용이며, 개인별 차이가 존재합니다.")
