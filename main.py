import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide",
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")
st.write("KOBIS 영화 데이터를 이용해 장르별 영화 편수의 분포를 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르에 여러 값이 있으면 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    df.loc[df["genre_first"].eq(""), "genre_first"] = "미상"
    return df


try:
    df = load_data()

    st.subheader("1. 장르별 영화 편수")

    genre_counts = (
        df["genre_first"]
        .value_counts()
        .rename_axis("장르")
        .reset_index(name="영화 편수")
    )

    fig = px.pie(
        genre_counts,
        names="장르",
        values="영화 편수",
        hole=0.55,
        title="장르별 영화 편수",
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>편수: %{value}편<br>비율: %{percent}<extra></extra>",
    )

    fig.update_layout(
        legend_title_text="장르",
        margin=dict(t=70, b=20, l=20, r=20),
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 이 그래프로 알 수 있는 것")
    st.info("장르별로 영화가 몇 편씩 분포되어 있는지와 전체 영화에서 각 장르가 차지하는 비율을 알 수 있습니다.")

except Exception as e:
    st.error("데이터를 불러오는 중 오류가 발생했습니다.")
    st.code(str(e))
