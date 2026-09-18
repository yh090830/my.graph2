# ==============================
# 8번 그래프
# 왕과 사는 남자의 관객 수가 가장 많이 몰린 달
# ==============================

streamlit.header("8. 왕과 사는 남자의 월별 관객 수")

try:
    daily_data = load_daily_data()

    # 컬럼명 확인
    movie_column = None
    for column in ["movieNm", "movie_name", "movie_name_kor"]:
        if column in daily_data.columns:
            movie_column = column
            break

    date_column = None
    for column in ["date", "showDt", "show_date"]:
        if column in daily_data.columns:
            date_column = column
            break

    audience_column = None
    for column in ["daily_audi", "dailyAudience", "daily_audience"]:
        if column in daily_data.columns:
            audience_column = column
            break

    if movie_column is None:
        streamlit.error("영화 이름 컬럼을 찾을 수 없습니다.")

    elif date_column is None:
        streamlit.error("날짜 컬럼을 찾을 수 없습니다.")

    elif audience_column is None:
        streamlit.error("일일 관객 수 컬럼을 찾을 수 없습니다.")

    else:
        target = daily_data[
            daily_data[movie_column]
            .astype(str)
            .str.contains("왕과 사는 남자", regex=False, na=False)
        ].copy()

        if target.empty:
            streamlit.warning(
                "해당 영화의 데이터를 찾지 못했습니다. "
                "영화 제목이 데이터에 있는지 확인해 주세요."
            )

        else:
            target["날짜"] = pd.to_datetime(
                target[date_column].astype(str).str.replace(".0", "", regex=False),
                format="%Y%m%d",
                errors="coerce"
            )

            # YYYY-MM-DD 형식도 추가로 처리
            missing_date = target["날짜"].isna()

            target.loc[missing_date, "날짜"] = pd.to_datetime(
                target.loc[missing_date, date_column],
                errors="coerce"
            )

            target["관객 수"] = (
                target[audience_column]
                .astype(str)
                .str.replace(",", "", regex=False)
            )

            target["관객 수"] = pd.to_numeric(
                target["관객 수"],
                errors="coerce"
            )

            target = target.dropna(subset=["날짜", "관객 수"])

            if target.empty:
                streamlit.warning("날짜 또는 관객 수 데이터를 읽을 수 없습니다.")

            else:
                target["월"] = target["날짜"].dt.month

                monthly_audience = (
                    target.groupby("월", as_index=False)["관객 수"]
                    .sum()
                    .sort_values("월")
                )

                monthly_audience["월"] = (
                    monthly_audience["월"].astype(str) + "월"
                )

                fig8 = px.bar(
                    monthly_audience,
                    x="월",
                    y="관객 수",
                    title="왕과 사는 남자의 월별 누적 관객 수",
                    labels={
                        "월": "월",
                        "관객 수": "관객 수"
                    },
                    text_auto=True
                )

                fig8.update_layout(
                    xaxis_title="월",
                    yaxis_title="관객 수",
                    xaxis_categoryorder="array",
                    xaxis_categoryarray=[
                        "1월", "2월", "3월", "4월",
                        "5월", "6월", "7월", "8월",
                        "9월", "10월", "11월", "12월"
                    ]
                )

                streamlit.plotly_chart(
                    fig8,
                    use_container_width=True
                )

                max_month = monthly_audience.loc[
                    monthly_audience["관객 수"].idxmax()
                ]

                streamlit.info(
                    f"관객 수가 가장 많이 몰린 달은 "
                    f"**{max_month['월']}**입니다."
                )

except Exception as error:
    streamlit.error("8번 그래프를 만드는 중 오류가 발생했습니다.")
    streamlit.code(str(error))
