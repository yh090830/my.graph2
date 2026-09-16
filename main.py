import streamlit
import pandas as pd
import plotly.express as px

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

streamlit.title("영화 데이터 그래프 도감 2 - 분포와 관계")
streamlit.write("KOBIS 영화 데이터를 이용해 영화 데이터의 분포와 관계를 살펴봅니다.")


@streamlit.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 |로 적혀 있으면 첫 번째 장르만 사용
    df["genre_first"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )
    df.loc[df["genre_first"] == "", "genre_first"] = "미상"

    # 총 관객 수를 숫자로 변환
    df["total_audi"] = (
        df["total_audi"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["total_audi"] = pd.to_numeric(
        df["total_audi"], errors="coerce"
    ).fillna(0)

    # 개봉일 스크린 수를 숫자로 변환
    df["first_scrn"] = (
        df["first_scrn"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"], errors="coerce"
    ).fillna(0)

    df["movieNm"] = df["movieNm"].fillna("영화명 미상").astype(str)

    return df


try:
    df = load_data()

    # 1. 장르별 영화 편수
    streamlit.subheader("1. 장르별 영화 편수")

    genre_counts = (
        df["genre_first"]
        .value_counts()
        .rename_axis("장르")
        .reset_index(name="영화 편수")
    )

    fig1 = px.pie(
        genre_counts,
        names="장르",
        values="영화 편수",
        hole=0.55,
        title="장르별 영화 편수",
    )

    fig1.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "편수: %{value}편<br>"
            "비율: %{percent}"
            "<extra></extra>"
        ),
    )

    streamlit.plotly_chart(fig1, use_container_width=True)

    streamlit.markdown("### 이 그래프로 알 수 있는 것")
    streamlit.info(
        "장르별로 영화가 몇 편씩 분포되어 있는지와 각 장르가 차지하는 비율을 알 수 있습니다."
    )

    # 2. 장르 안에 영화가 들어 있는 트리맵
    streamlit.markdown("---")
    streamlit.subheader("2. 장르 안에 영화가 들어 있는 트리맵")

    treemap_df = df[["genre_first", "movieNm", "total_audi"]].copy()

    fig2 = px.treemap(
        treemap_df,
        path=["genre_first", "movieNm"],
        values="total_audi",
        title="장르별 영화와 총 관객",
    )

    fig2.update_traces(
        hovertemplate=(
            "<b>%{label}</b><br>"
            "총 관객: %{value:,.0f}명"
            "<extra></extra>"
        )
    )

    streamlit.plotly_chart(fig2, use_container_width=True)

    streamlit.markdown("### 이 그래프로 알 수 있는 것")
    streamlit.info(
        "장르별로 어떤 영화가 포함되어 있는지와 영화별 총 관객 규모의 차이를 알 수 있습니다."
    )

    # 3. 총 관객 수 히스토그램
    streamlit.markdown("---")
    streamlit.subheader("3. 총 관객 수 분포")

    fig3 = px.histogram(
        df,
        x="total_audi",
        nbins=30,
        title="영화별 총 관객 수 분포",
        labels={
            "total_audi": "총 관객 수",
            "count": "영화 편수"
        }
    )

    streamlit.plotly_chart(fig3, use_container_width=True)

    bins = pd.cut(df["total_audi"], bins=30)
    most_common_bin = bins.value_counts().idxmax()

    max_idx = df["total_audi"].idxmax()
    max_movie = df.loc[max_idx, "movieNm"]
    max_audi = df.loc[max_idx, "total_audi"]

    streamlit.markdown("### 이 그래프로 알 수 있는 것")
    streamlit.info(
        f"대부분의 영화는 총 관객 수가 "
        f"{most_common_bin.left:,.0f}명 ~ "
        f"{most_common_bin.right:,.0f}명 구간에 몰려 있습니다. "
        f"가장 관객이 많은 영화는 **{max_movie}**이며, "
        f"총 관객 수는 **{max_audi:,.0f}명**입니다."
    )

    # 4. 개봉일 스크린 수와 총 관객의 관계
    streamlit.markdown("---")
    streamlit.subheader("4. 개봉일 스크린 수와 총 관객의 관계")

    fig4 = px.scatter(
        df,
        x="first_scrn",
        y="total_audi",
        color="genre_first",
        hover_name="movieNm",
        title="개봉일 스크린 수와 총 관객의 관계",
        labels={
            "first_scrn": "개봉일 스크린 수",
            "total_audi": "총 관객",
            "genre_first": "장르"
        }
    )

    streamlit.plotly_chart(fig4, use_container_width=True)

    streamlit.markdown("### 이 그래프로 알 수 있는 것")
    streamlit.info(
        "개봉일 스크린 수와 총 관객의 관계를 알 수 있으며, "
        "장르별로 점의 색이 다르게 표시됩니다."
    )

except Exception as e:
    streamlit.error("데이터를 불러오거나 그래프를 만드는 중 오류가 발생했습니다.")
    streamlit.code(str(e))
