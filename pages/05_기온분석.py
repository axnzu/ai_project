import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="서울 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 특정 날짜 연도별 최고·최저기온 분석")

@st.cache_data
def load_data():

    # 여러 인코딩 시도
    encodings = ["cp949", "euc-kr", "utf-8"]

    df = None

    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            break
        except:
            continue

    if df is None:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.stop()

    # 컬럼명 정리
    df.columns = df.columns.str.strip()

    # BOM 제거
    df.columns = [col.replace("\ufeff", "") for col in df.columns]

    # 날짜 컬럼 찾기
    date_col = None

    for col in df.columns:
        if "날짜" in col:
            date_col = col
            break

    if date_col is None:
        st.error(f"날짜 컬럼을 찾을 수 없습니다. 현재 컬럼: {list(df.columns)}")
        st.stop()

    # 날짜 변환
    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
        format="mixed"
    )

    # 날짜 오류 제거
    df = df.dropna(subset=[date_col])

    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df


df = load_data()

# 최고기온 컬럼 찾기
max_col = None
min_col = None

for col in df.columns:
    if "최고기온" in col:
        max_col = col
    if "최저기온" in col:
        min_col = col

if max_col is None or min_col is None:
    st.error(
        f"최고기온/최저기온 컬럼을 찾을 수 없습니다.\n현재 컬럼: {list(df.columns)}"
    )
    st.stop()

# 월 선택
month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

# 해당 월의 일 목록
days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    days
)

# 필터링
filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

st.subheader(f"📅 {month}월 {day}일 연도별 기온")

if filtered.empty:

    st.warning("해당 날짜 데이터가 없습니다.")

else:

    fig = go.Figure()

    # 최고기온 (분홍색)
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"],
            y=filtered[max_col],
            mode="lines+markers",
            name="최고기온",
            line=dict(
                color="#FF69B4",
                width=3
            ),
            marker=dict(
                size=7,
                color="#FF69B4"
            )
        )
    )

    # 최저기온 (연한 파란색)
    fig.add_trace(
        go.Scatter(
            x=filtered["연도"],
            y=filtered[min_col],
            mode="lines+markers",
            name="최저기온",
            line=dict(
                color="#87CEFA",
                width=3
            ),
            marker=dict(
                size=7,
                color="#87CEFA"
            )
        )
    )

    fig.update_layout(
        title=f"{month}월 {day}일 연도별 최고·최저기온",
        xaxis_title="연도",
        yaxis_title="기온 (℃)",
        hovermode="x unified",
        height=700,
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
            ["연도", min_col, max_col]
        ].rename(
            columns={
                min_col: "최저기온(℃)",
                max_col: "최고기온(℃)"
            }
        ),
        use_container_width=True
    )
