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

# MBTI 컬럼
mbti_cols = [col for col in df.columns if col != "Country"]

# -----------------------------
# 색상 함수
# -----------------------------
def generate_green_gradient(values):
    max_value = max(values)

    colors = []

    for value in values:
        if value == max_value:
            # 1등은 진한 초록색
            colors.append("rgb(0, 128, 0)")
        else:
            # 연한 초록 ~ 진한 초록
            alpha = 0.2 + (value / max_value) * 0.8
            colors.append(f"rgba(34, 139, 34, {alpha})")

    return colors

# -----------------------------
# 탭 생성
# -----------------------------
tab1, tab2 = st.tabs([
    "📊 국가별 MBTI 분석",
    "🏆 MBTI별 국가 TOP 10"
])

# ==================================================
# TAB 1 : 국가 선택
# ==================================================
with tab1:

    st.header("📊 국가별 MBTI 비율")

    countries = sorted(df["Country"].unique())

    selected_country = st.selectbox(
        "국가를 선택하세요",
        countries
    )

    # 선택 국가 데이터
    country_data = df[df["Country"] == selected_country].iloc[0]

    # 데이터 정렬
    result_df = pd.DataFrame({
        "MBTI": mbti_cols,
        "Ratio": [country_data[col] for col in mbti_cols]
    })

    result_df = result_df.sort_values(
        by="Ratio",
        ascending=False
    )

    # 색상 생성
    colors = generate_green_gradient(result_df["Ratio"].values)

    # 그래프 생성
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=result_df["MBTI"],
            y=result_df["Ratio"],
            marker_color=colors,
            text=[f"{v:.2%}" for v in result_df["Ratio"]],
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

    st.subheader("📋 MBTI 순위")

    display_df = result_df.copy()
    display_df["Ratio"] = display_df["Ratio"].apply(
        lambda x: f"{x:.2%}"
    )

    st.dataframe(
        display_df,
        use_container_width=True
    )

# ==================================================
# TAB 2 : MBTI 선택
# ==================================================
with tab2:

    st.header("🏆 MBTI별 국가 TOP 10")

    selected_mbti = st.selectbox(
        "MBTI를 선택하세요",
        mbti_cols
    )

    # TOP 10 국가 추출
    top10_df = df[["Country", selected_mbti]].sort_values(
        by=selected_mbti,
        ascending=False
    ).head(10)

    # 색상 생성
    colors = generate_green_gradient(
        top10_df[selected_mbti].values
    )

    # 그래프 생성
    fig2 = go.Figure()

    fig2.add_trace(
        go.Bar(
            x=top10_df["Country"],
            y=top10_df[selected_mbti],
            marker_color=colors,
            text=[
                f"{v:.2%}"
                for v in top10_df[selected_mbti]
            ],
            textposition="outside"
        )
    )

    fig2.update_layout(
        title=f"Top 10 Countries for {selected_mbti}",
        xaxis_title="Country",
        yaxis_title="Ratio",
        height=600,
        template="plotly_white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📋 TOP 10 국가")

    display_top10 = top10_df.copy()

    display_top10[selected_mbti] = display_top10[
        selected_mbti
    ].apply(lambda x: f"{x:.2%}")

    st.dataframe(
        display_top10,
        use_container_width=True
    )
