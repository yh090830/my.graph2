import streamlit as st
import pandas as pd
import plotly.express as px


MOVIES_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"
DAILY_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


st.set_page_config(
    page_title="영화 데이터 그래프 도감 2",
    layout="wide"
)


@st.cache_data
def load_movies():
    return pd.read_csv(MOVIES_URL)


@st.cache_data
def load_daily():
    return pd.read_csv(DAILY_URL)


def convert_number(data, column):
    if column in data.columns:
        data[column] = pd.to_numeric(
            data[column]
            .astype(str)
            .str.replace(",", "", regex=False),
            errors="coerce"
        )
    return data


try:
    movies = load_movies()

    st.title("영화 데이터 그래프 도감 2 - 분포와 관계")


    # ==============================
    # 데이터 전처리
    # ==============================

    required_columns = [
        "movieNm",
        "genre",
        "nation",
        "total_audi",
        "first_scrn",
        "first_week_audi"
    ]

    missing = [
        column for column in required_columns
        if column not in movies.columns
    ]

    if missing:
        st.error("영화 데이터의 컬럼을 확인할 수 없습니다.")
        st.write("없는 컬럼:", missing)
        st.write("현재 컬럼:", list(movies.columns))
        st.stop()

    movies["genre_first"] = (
        movies["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    movies["nation_first"] = (
        movies["nation"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
    )

    for column in [
        "total_audi",
        "first_scrn",
        "first_week_audi",
        "first_show",
        "days_in_top10"
    ]:
        movies = convert_number(movies, column)

    movies = movies.dropna(subset=["total_audi"])


    # ==============================
    # 1번 그래프
    # ==============================

    st.header("1. 장르별 영화 수")

    genre_count = (
        movies["genre_first"]
        .value_counts()
        .reset_index()
    )

    genre_count.columns = ["장르", "영화 수"]

    fig1 = px.pie(
        genre_count,
        names="장르",
        values="영화 수",
        hole=0.4,
        title="장르별 영화 수"
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.info(
        "알 수 있는 것: 어떤 장르의 영화가 가장 많이 분포하는지 알 수 있습니다."
    )


    # ==============================
    # 2번 그래프
    # ==============================

    st.header("2. 장르별 영화 관객 수 트리맵")

    treemap_data = movies[
        ["genre_first", "movieNm", "total_audi"]
    ].dropna()

    fig2 = px.treemap(
        treemap_data,
        path=["genre_first", "movieNm"],
        values="total_audi",
        title="장르와 영화별 총 관객 수"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "알 수 있는 것: 장르별로 어떤 영화가 많은 관객을 모았는지 비교할 수 있습니다."
    )


    # ==============================
    # 3번 그래프
    # ==============================

    st.header("3. 총 관객 수 분포")

    fig3 = px.histogram(
        movies,
        x="total_audi",
        nbins=30,
        title="영화별 총 관객 수 분포",
        labels={"total_audi": "총 관객 수"}
    )

    st.plotly_chart(fig3, use_container_width=True)

    max_movie = movies.loc[
        movies["total_audi"].idxmax(),
        "movieNm"
    ]

    max_audience = movies["total_audi"].max()

    st.info(
        f"알 수 있는 것: 가장 관객이 많은 영화는 "
        f"**{max_movie}**이며, 총 관객 수는 "
        f"**{max_audience:,.0f}명**입니다."
    )


    # ==============================
    # 4번 그래프
    # ==============================

    st.header("4. 첫 상영 스크린 수와 총 관객 수")

    scatter_data = movies.dropna(
        subset=["first_scrn", "total_audi", "genre_first"]
    )

    fig4 = px.scatter(
        scatter_data,
        x="first_scrn",
        y="total_audi",
        color="genre_first",
        hover_name="movieNm",
        title="첫 상영 스크린 수와 총 관객 수의 관계",
        labels={
            "first_scrn": "첫 상영 스크린 수",
            "total_audi": "총 관객 수",
            "genre_first": "장르"
        }
    )

    st.plotly_chart(fig4, use_container_width=True)

    st.info(
        "알 수 있는 것: 첫 상영 스크린 수와 총 관객 수 사이의 관계를 확인할 수 있습니다."
    )


    # ==============================
    # 5번 그래프
    # ==============================

    st.header("5. 장르별 총 관객 수 박스플롯")

    genre_counts = movies["genre_first"].value_counts()

    valid_genres = genre_counts[
        genre_counts >= 10
    ].index

    box_data = movies[
        movies["genre_first"].isin(valid_genres)
    ].dropna(
        subset=["genre_first", "total_audi"]
    )

    if box_data.empty:
        st.warning("영화가 10편 이상인 장르가 없습니다.")

    else:
        fig5 = px.box(
            box_data,
            x="genre_first",
            y="total_audi",
            points="outliers",
            hover_name="movieNm",
            title="영화가 10편 이상인 장르의 총 관객 수",
            labels={
                "genre_first": "장르",
                "total_audi": "총 관객 수"
            }
        )

        st.plotly_chart(fig5, use_container_width=True)

    st.info(
        "알 수 있는 것: 장르별 총 관객 수의 분포와 특이값을 확인할 수 있습니다."
    )


    # ==============================
    # 6번 그래프
    # ==============================

    st.header("6. 첫 스크린 수와 총 관객 수 버블 차트")

    bubble_data = movies.dropna(
        subset=[
            "first_scrn",
            "total_audi",
            "first_week_audi",
            "genre_first"
        ]
    ).copy()

    bubble_data["first_week_audi"] = bubble_data[
        "first_week_audi"
    ].clip(lower=1)

    fig6 = px.scatter(
        bubble_data,
        x="first_scrn",
        y="total_audi",
        color="genre_first",
        size="first_week_audi",
        hover_name="movieNm",
        title="첫 스크린 수와 총 관객 수 버블 차트",
        labels={
            "first_scrn": "첫 상영 스크린 수",
            "total_audi": "총 관객 수",
            "first_week_audi": "첫 주 관객 수",
            "genre_first": "장르"
        }
    )

    st.plotly_chart(fig6, use_container_width=True)

    st.info(
        "알 수 있는 것: 버블 크기로 영화의 첫 주 관객 수를 비교할 수 있습니다."
    )


    # ==============================
    # 7번 그래프
    # ==============================

    st.header("7. 국가별·장르별 영화 분포")

    sunburst_data = (
        movies.groupby(
            ["nation_first", "genre_first"],
            as_index=False
        )
        .size()
        .rename(columns={"size": "영화 수"})
    )

    fig7 = px.sunburst(
        sunburst_data,
        path=["nation_first", "genre_first"],
        values="영화 수",
        title="국가별·장르별 영화 수"
    )

    st.plotly_chart(fig7, use_container_width=True)

    st.info(
        "알 수 있는 것: 국가별 영화 제작 분포와 장르 구성을 확인할 수 있습니다."
    )


    # ==============================
    # 8번 그래프
    # ==============================

    st.header("8. 왕과 사는 남자의 월별 관객 수")

    daily = load_daily()

    daily_required = [
        "날짜",
        "영화명",
        "일관객"
    ]

    daily_missing = [
        column for column in daily_required
        if column not in daily.columns
    ]

    if daily_missing:
        st.error("일일 영화 데이터의 컬럼을 확인할 수 없습니다.")
        st.write("없는 컬럼:", daily_missing)
        st.write("현재 컬럼:", list(daily.columns))
        st.stop()

    target = daily[
        daily["영화명"]
        .astype(str)
        .str.contains(
            "왕과 사는 남자",
            regex=False,
            na=False
        )
    ].copy()

    if target.empty:
        st.warning(
            "왕과 사는 남자에 해당하는 데이터를 찾지 못했습니다."
        )

    else:
        # 날짜 변환
        date_text = (
            target["날짜"]
            .astype(str)
            .str.replace(".0", "", regex=False)
            .str.strip()
        )

        target["날짜_변환"] = pd.to_datetime(
            date_text,
            format="%Y%m%d",
            errors="coerce"
        )

        invalid_dates = target["날짜_변환"].isna()

        if invalid_dates.any():
            target.loc[
                invalid_dates,
                "날짜_변환"
            ] = pd.to_datetime(
                date_text[invalid_dates],
                errors="coerce"
            )

        # 관객 수 변환
        target["관객 수"] = pd.to_numeric(
            target["일관객"]
            .astype(str)
            .str.replace(",", "", regex=False),
            errors="coerce"
        )

        target = target.dropna(
            subset=["날짜_변환", "관객 수"]
        )

        if target.empty:
            st.warning(
                "날짜 또는 관객 수 데이터를 읽지 못했습니다."
            )

        else:
            target["월"] = target["날짜_변환"].dt.month

            monthly = (
                target.groupby("월", as_index=False)["관객 수"]
                .sum()
                .sort_values("월")
            )

            monthly["월 표시"] = (
                monthly["월"].astype(int).astype(str) + "월"
            )

            fig8 = px.bar(
                monthly,
                x="월 표시",
                y="관객 수",
                text="관객 수",
                title="왕과 사는 남자의 월별 관객 수",
                labels={
                    "월 표시": "월",
                    "관객 수": "관객 수"
                }
            )

            fig8.update_traces(
                texttemplate="%{text:,.0f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig8,
                use_container_width=True
            )

            max_row = monthly.loc[
                monthly["관객 수"].idxmax()
            ]

            st.info(
                f"알 수 있는 것: 왕과 사는 남자의 관객 수가 "
                f"가장 많이 몰린 달은 "
                f"**{int(max_row['월'])}월**입니다."
            )


except Exception as error:
    st.error("프로그램 실행 중 오류가 발생했습니다.")
    st.code(str(error))
