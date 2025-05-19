import plotly.express as px

def create_educational_area_bar(df, educational_area, num_years=5):
    filtered = (
        df[df["Utbildningsinriktning"] == educational_area]
        .groupby("År")["Antal studerande"]
        .sum()
        .reset_index()
        .sort_values(by="År", ascending=False)
        .head(num_years)
        .sort_values(by="År")
    )

    fig = px.bar(
        filtered,
        x="År",
        y="Antal studerande",
        title=None,
        labels={"Antal studerande": "Antal studerande", "År": "År"},
    )
    fig.update_layout(xaxis=dict(tickangle=45))
    return fig
