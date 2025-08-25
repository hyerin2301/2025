import streamlit as st
from datetime import datetime, time, timedelta

# -----------------------------
# 기본 설정 & 스타일
# -----------------------------
st.set_page_config(page_title="개운하게 기상 ⏰ 취침 시간 계산기", page_icon="😴", layout="centered")

st.markdown(
    """
    <style>
    .title {
        text-align:center; 
        font-size: 36px; 
        font-weight: 800; 
        color: #6C63FF;
    }
    .subtitle {
        text-align:center; 
        color:#666; 
        margin-top: -10px;
    }
    .pill {
        border-radius: 16px;
        padding: 14px 18px;
        margin: 8px 0;
        border: 1px solid #eee;
        box-shadow: 0 6px 18px rgba(0,0,0,0.06);
        background: white;
    }
    .badge {
        display:inline-block;
        padding: 4px 10px; 
        border-radius: 999px; 
        background:#F0EDFF; 
        color:#6C63FF; 
        font-weight:700; 
        margin-right:8px;
    }
    .time-big {
        font-size: 28px; 
        font-weight: 800; 
        color:#222;
        letter-spacing: 0.5px;
    }
    .tip {
        background: #FFF8E7;
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

st.markdown("<div class='title'>개운하게 일어나려면 언제 자야 할까? ⏰</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>수면 주기(약 90분)와 입면 시간(잠드는 데 걸리는 시간)을 반영해 권장 취침 시각을 계산해 드려요.</div>", unsafe_allow_html=True)
st.markdown("")

# -----------------------------
# 입력 영역
# -----------------------------
with st.container():
    st.markdown("### 💡 입력")
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
        wake_time = st.time_input("기상 시각", value=time(7, 0), help="아침에 일어나고 싶은(혹은 일어나야 하는) 시간을 선택하세요.")
    with col2:
        fall_asleep_min = st.slider("잠드는 데 걸리는 시간(분)", 0, 40, 15, step=5, help="평균적으로 잠드는 데 걸리는 시간을 선택하세요. 기본 15분")
    with col3:
        cycle_min = st.slider("수면 주기 길이(분)", 80, 100, 90, step=1, help="개인차가 있어요. 보통 90분 전후입니다.")

    st.caption("🔁 권장 계산 주기: 3~6주기 (4~5주기 권장) — 너무 과도한 수면도 컨디션을 떨어뜨릴 수 있어요.")

# -----------------------------
# 계산 함수
# -----------------------------
def compute_bedtimes(wake_t: time, fall_min: int, cycle_len: int, cycles=(3,4,5,6)):
    """
    wake_t: 기상 시각 (datetime.time)
    fall_min: 입면 시간 (분)
    cycle_len: 수면 주기 길이 (분)
    cycles: 계산할 주기들
    return: [(n주기, 취침 datetime), ...] 최근 시간 순으로 정렬
    """
    # 오늘 날짜 기준으로 datetime 구성 (날짜는 의미 없음, 계산용)
    base_date = datetime.combine(datetime.today().date(), wake_t)
    results = []
    for n in cycles:
        total_min = fall_min + cycle_len * n
        bedtime = base_date - timedelta(minutes=total_min)
        results.append((n, bedtime))
    # 최근(늦은) 취침시간이 위로 오도록 정렬
    results.sort(key=lambda x: x[1], reverse=True)
    return results

cycles_to_show = (3,4,5,6)
results = compute_bedtimes(wake_time, fall_asleep_min, cycle_min, cycles_to_show)

# -----------------------------
# 출력 영역
# -----------------------------
st.markdown("### 🎯 권장 취침 시각")

cards = st.columns(len(results))
for idx, (n, bt) in enumerate(results):
    with cards[idx]:
        # 취침 시각 표기 (날짜 포함 표기 + 전날 표기)
        label_date = bt.strftime("%m/%d (%a)")
        label_time = bt.strftime("%H:%M")
        # 기상 시각 표기
        wake_label = datetime.combine(datetime.today().date(), wake_time).strftime("%H:%M")

        st.markdown(
            f"""
            <div class="pill">
                <div class="badge">{n}주기 수면</div>
                <div class="time-big">🛏️ {label_time}</div>
                <div style="color:#777; margin-top:4px;">취침 날짜: {label_date}</div>
                <hr style="border:none; border-top:1px solid #f2f2f2; margin:10px 0;">
                <div>⏱️ 입면: 약 {fall_asleep_min}분</div>
                <div>🔁 주기: {cycle_min}분 × {n}</div>
                <div>⏰ 기상: {wake_label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# 베스트 추천 설명
best = sorted(results, key=lambda x: abs(x[0]-5))[0]  # 5주기에 가장 가깝게
best_time = best[1].strftime("%H:%M")
st.markdown(
    f"""
    <div class="tip" style="margin-top:10px;">
        ✅ <b>추천</b>: 보통 <b>4~5주기</b> (약 6~7.5시간 수면)을 많이 권장해요.  
        현재 설정이라면 <b>{best[0]}주기</b> 기준 <b>{best_time}</b> 취침이 가장 무난합니다.
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 추가 기능: 역방향 계산 (선택)
# -----------------------------
with st.expander("🔄 (선택) 취침 시각을 아는 경우 → 개운한 기상 시각 계산하기"):
    bt_input = st.time_input("취침 시각", value=time(23, 0))
    cycles_back = st.multiselect("계산할 주기(깨어날 시각)", [3,4,5,6], default=[4,5])
    calc_btn = st.button("기상 시각 계산하기")
    if calc_btn and cycles_back:
        base_bt = datetime.combine(datetime.today().date(), bt_input)
        cols = st.columns(len(cycles_back))
        for i, cyc in enumerate(sorted(cycles_back)):
            with cols[i]:
                wake_dt = base_bt + timedelta(minutes=fall_asleep_min + cycle_min * cyc)
                st.markdown(
                    f"""
                    <div class="pill">
                        <div class="badge">{cyc}주기 후</div>
                        <div class="time-big">🌅 {wake_dt.strftime("%H:%M")}</div>
                        <div style="color:#777; margin-top:4px;">기상 날짜: {wake_dt.strftime("%m/%d (%a)")}</div>
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
    - 입면 시간이 길어지는 날(스트레스/카페인)은 **슬라이더로 입면 분**을 늘려서 계산해 보세요.  
    - 주기 길이는 개인차가 있으니 **85~95분** 사이에서 몸에 잘 맞는 값을 찾아보면 더 정확해요.  
    - 주말이라도 기상 시각을 크게 바꾸지 않으면 **월요일 컨디션**이 좋아져요.  
    """
)

st.caption("⚠️ 본 계산기는 일반적인 수면 주기 모델을 따른 참고용 도구이며, 개인별 차이가 존재합니다.")
