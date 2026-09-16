try:
    df = load_data()

    # 3. 총 관객 수 히스토그램
    streamlit.markdown("---")
    streamlit.subheader("3. 총 관객 수 분포")

    fig3 = px.histogram(
        df,
        x="total_audi",
        nbins=30,
        title="영화별 총 관객 수 분포"
    )

    streamlit.plotly_chart(fig3, use_container_width=True)
