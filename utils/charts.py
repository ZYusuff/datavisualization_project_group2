import plotly.express as px
import plotly.graph_objects as go

def create_educational_area_bar(df, selected_area, num_years=5):
    # Filtrera de senaste num_years åren
    recent_years = sorted(df["År"].unique())[-num_years:]
    filtered = df[df["År"].isin(recent_years)]

    # Summera per inriktning och år
    grouped = (
        filtered.groupby(["År", "Utbildningsinriktning"])["Antal studerande"]
        .sum()
        .reset_index()
    )

    # Skapa grundgraf med alla utbildningsområden
    fig = go.Figure()

    for area in grouped["Utbildningsinriktning"].unique():
        area_data = grouped[grouped["Utbildningsinriktning"] == area]
        fig.add_trace(
            go.Scatter(
                x=area_data["År"],
                y=area_data["Antal studerande"],
                mode="lines+markers",
                name=area,
                line=dict(
                    width=4 if area == selected_area else 1.5,
                    color="#0077b6" if area == selected_area else "#cccccc"
                ),
                marker=dict(size=6 if area == selected_area else 4),
                opacity=1.0 if area == selected_area else 0.4,
                hovertemplate=f"{area}<br>År: %{{x}}<br>Antal studerande: %{{y}}<extra></extra>",
            )
        )

    fig.update_layout(
        title=None,
        xaxis=dict(title="År", tickangle=0, title_font=dict(size=14), tickfont=dict(size=12)),
        yaxis=dict(title="Antal studerande", title_font=dict(size=14), tickfont=dict(size=12)),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(family="Arial", size=14),
        margin=dict(t=20, b=40, l=60, r=20),
        hovermode="x unified",
        showlegend=False,
    )

    return fig
