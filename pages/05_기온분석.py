import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("🌡️ 서울 특정 날짜 연도별 기온 변화")

@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="cp949")

    df["날짜"] = pd.to_datetime(df["날짜"])

    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 월 선택
month = st.selectbox(
    "월 선택",
    options=range(1, 13)
)

# 해당 월의 실제 존재하는 일만 표시
available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    options=available_days
)

# 데이터 필터링
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

st.subheader(f"📅 {month}월 {day}일 연도별 기온")

if filtered.empty:
    st.warning("데이터가 없습니다.")
else:

    fig = go.Figure()

    # 최고기온 (분홍색)
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"],
            y=filtered["최고기온(℃)"],
            mode="lines+markers",
            name="최고기온",
            line=dict(
                color="#ff69b4",
                width=3
            ),
            marker=dict(
                color="#ff69b4",
                size=7
            )
        )
    )

    # 최저기온 (연한 파란색)
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"],
            y=filtered["최저기온(℃)"],
            mode="lines+markers",
            name="최저기온",
            line=dict(
                color="#87cefa",
                width=3
            ),
            marker=dict(
                color="#87cefa",
                size=7
            )
        )
    )

    fig.update_layout(
        title=f"{month}월 {day}일 연도별 최고·최저기온",
        xaxis_title="연도",
        yaxis_title="기온(℃)",
        hovermode="x unified",
        height=650,
        legend=dict(
            orientation="h",
            y=1.05,
            x=0
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        filtered[
            [
                "연도",
                "최저기온(℃)",
                "최고기온(℃)"
            ]
        ],
        use_container_width=True
    )
