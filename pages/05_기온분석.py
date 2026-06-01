import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="서울 기온 예측",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 서울 특정 날짜 기온 분석 및 미래 예측")

@st.cache_data
def load_data():

    encodings = ["cp949", "euc-kr", "utf-8"]

    df = None

    for enc in encodings:
        try:
            df = pd.read_csv("seoul.csv", encoding=enc)
            break
        except:
            pass

    if df is None:
        st.error("CSV 파일을 읽을 수 없습니다.")
        st.stop()

    df.columns = df.columns.str.strip()
    df.columns = [c.replace("\ufeff", "") for c in df.columns]

    date_col = None

    for c in df.columns:
        if "날짜" in c:
            date_col = c
            break

    if date_col is None:
        st.error("날짜 컬럼을 찾을 수 없습니다.")
        st.stop()

    df[date_col] = pd.to_datetime(
        df[date_col],
        errors="coerce",
        format="mixed"
    )

    df = df.dropna(subset=[date_col])

    df["연도"] = df[date_col].dt.year
    df["월"] = df[date_col].dt.month
    df["일"] = df[date_col].dt.day

    return df

df = load_data()

max_col = [c for c in df.columns if "최고기온" in c][0]
min_col = [c for c in df.columns if "최저기온" in c][0]

month = st.selectbox(
    "월 선택",
    sorted(df["월"].unique())
)

days = sorted(
    df[df["월"] == month]["일"].unique()
)

day = st.selectbox(
    "일 선택",
    days
)

future_year = st.number_input(
    "예측할 미래 연도",
    min_value=int(df["연도"].max()) + 1,
    max_value=2100,
    value=2030
)

filtered = df[
    (df["월"] == month) &
    (df["일"] == day)
].copy()

filtered = filtered.sort_values("연도")

if filtered.empty:
    st.warning("데이터가 없습니다.")
    st.stop()

X = filtered["연도"].values.reshape(-1, 1)

# 최고기온 모델
max_model = make_pipeline(
    PolynomialFeatures(degree=3),
    LinearRegression()
)

max_model.fit(
    X,
    filtered[max_col]
)

pred_max = max_model.predict(
    [[future_year]]
)[0]

# 최저기온 모델
min_model = make_pipeline(
    PolynomialFeatures(degree=3),
    LinearRegression()
)

min_model.fit(
    X,
    filtered[min_col]
)

pred_min = min_model.predict(
    [[future_year]]
)[0]

st.subheader(
    f"📅 {month}월 {day}일 미래 기온 예측"
)

col1, col2 = st.columns(2)

with col1:
    st.metric(
        f"{future_year}년 예상 최고기온",
        f"{pred_max:.1f}℃"
    )

with col2:
    st.metric(
        f"{future_year}년 예상 최저기온",
        f"{pred_min:.1f}℃"
    )

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered[max_col],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="#FF69B4",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered[min_col],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#87CEFA",
            width=3
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_max],
        mode="markers+text",
        name="예상 최고기온",
        text=[f"{pred_max:.1f}℃"],
        textposition="top center",
        marker=dict(
            size=14,
            color="red"
        )
    )
)

fig.add_trace(
    go.Scatter(
        x=[future_year],
        y=[pred_min],
        mode="markers+text",
        name="예상 최저기온",
        text=[f"{pred_min:.1f}℃"],
        textposition="bottom center",
        marker=dict(
            size=14,
            color="blue"
        )
    )
)

fig.update_layout(
    title=f"{month}월 {day}일 연도별 기온 및 미래 예측",
    xaxis_title="연도",
    yaxis_title="기온(℃)",
    hovermode="x unified",
    height=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(
    filtered[
        ["연도", min_col, max_col]
    ],
    use_container_width=True
)
