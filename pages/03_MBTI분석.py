import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="Countries MBTI Dashboard",
    layout="wide"
)

st.title("🌍 Countries MBTI Dashboard")

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# 국가 목록
countries = sorted(df["Country"].unique())

# 국가 선택
selected_country = st.selectbox(
    "국가를 선택하세요",
    countries
)

# 선택 국가 데이터
country_data = df[df["Country"] == selected_country].iloc[0]

# MBTI 컬럼
mbti_cols = [col for col in df.columns if col != "Country"]

# 값 추출
values = country_data[mbti_cols].values

# 최대값 찾기
max_value = max(values)

# 색상 설정
colors = []

# 하늘색 그라데이션
base_blue = [135, 206, 250]

for value in values:
    if value == max_value:
        # 1등은 노란색
        colors.append("rgb(255, 215, 0)")
    else:
        # 값 비율로 투명도 조절
        alpha = 0.3 + (value / max_value) * 0.7
        colors.append(f"rgba({base_blue[0]}, {base_blue[1]}, {base_blue[2]}, {alpha})")

# 그래프 생성
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=mbti_cols,
        y=values,
        marker_color=colors,
        text=[f"{v:.2%}" for v in values],
        textposition="outside"
    )
)

fig.update_layout(
    title=f"{selected_country} MBTI Distribution",
    xaxis_title="MBTI Type",
    yaxis_title="Ratio",
    height=600,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 테이블 표시
result_df = pd.DataFrame({
    "MBTI": mbti_cols,
    "Ratio": values
}).sort_values(by="Ratio", ascending=False)

st.subheader("📊 MBTI Ranking")
st.dataframe(result_df, use_container_width=True)
