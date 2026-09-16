    # 3. 총 관객 수 히스토그램
    streamlit.markdown("---")
    streamlit.subheader("3. 총 관객 수 분포")

    fig3 = px.histogram(
        df,
        x="total_audi",
        nbins=30,
        title="영화별 총 관객 수 분포",
        labels={"total_audi": "총 관객 수", "count": "영화 편수"},
    )

    fig3.update_traces(
        hovertemplate=(
            "총 관객 수: %{x:,.0f}명<br>"
            "영화 편수: %{y}편"
            "<extra></extra>"
        )
    )

    streamlit.plotly_chart(fig3, use_container_width=True)

    # 대부분의 영화가 몰려 있는 구간 계산
    counts, bins = pd.cut(
        df["total_audi"],
        bins=30,
        include_lowest=True,
        retbins=True
    )

    bin_counts = counts.value_counts().sort_index()
    most_common_bin = bin_counts.idxmax()

    # 가장 관객이 많은 영화
    max_idx = df["total_audi"].idxmax()
    max_movie = df.loc[max_idx, "movieNm"]
    max_audi = df.loc[max_idx, "total_audi"]

    streamlit.markdown("### 이 그래프로 알 수 있는 것")
    streamlit.info(
        f"대부분의 영화는 총 관객 수가 "
        f"{most_common_bin.left:,.0f}명 ~ {most_common_bin.right:,.0f}명 "
        f"구간에 몰려 있습니다. "
        f"가장 관객이 많은 영화는 **{max_movie}**로, "
        f"총 관객 수는 **{max_audi:,.0f}명**입니다."
    )
