import duckdb
import plotly.express as px
import plotly.graph_objects as go
from backend.data_processing.page_1_data_processing import map_df, geo_file


# CHARTS AND STATS FOR THE COURSE PAGE (PAGE 1)
# stats on top of course page
def course_stats(df, **options):
    if "year" in options:
        selected_year = options.get("year")
        total_count = duckdb.query(
            f"""--sql
                 SELECT COUNT(*) as count
                 FROM df
                WHERE "År" = {selected_year}
        """
        ).df()
        total_count = total_count.iloc[0, 0]
        total_approved = duckdb.query(
            f"""--sql
                SELECT COUNT(*) as count
                FROM df
                WHERE "År" = {selected_year} AND "Beslut" = 'Beviljad'
        """
        ).df()
        total_approved = total_approved.iloc[0, 0]
        approved_rate = total_approved / total_count
    return (total_count, total_approved, approved_rate)


# table for the course page
def course_school_table(df, school="", year=2024):
    if school == "":
        df = duckdb.query(
            f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS "Antal kurser",
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS "Beviljade kurser",
                "Beviljade kurser"/ "Antal kurser" AS rate
                FROM df
                WHERE "År" = {year}
                GROUP BY skola
                ORDER BY "Antal kurser" DESC
        """
        ).df()
        df["rate"] = round((df["rate"] * 100), 2).astype(str) + "%"
        df = df.rename(columns={"rate": "Beviljandegrad"})
        return df
    else:
        df = duckdb.query(
            f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year} AND skola = '{school}'
                GROUP BY skola  
                ORDER BY antal_kurser DESC
        """
        ).df()
        return df


# plot the bar chart for area of education
def plot_area(df, year):
    duckdb.register("df_for_query", df)
    plot_df = duckdb.query(
        f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal, Beslut
            FROM df
            WHERE År = {year}
            GROUP BY Utbildningsområde, Beslut
                        ORDER BY antal DESC
        """
    ).df()

    custom_colors = {
        "Beviljad": "#084083",  # Color for Approved
        "Avslag": "#E4ECF6",  # Color for Rejected
    }

    fig = px.bar(
        plot_df,
        x="antal",
        y="Utbildningsområde",
        color="Beslut",
        color_discrete_map=custom_colors,
        orientation="h",
        text_auto=True,
        height=800,
    )
    fig.update_layout(
        showlegend=False,
        barmode="group",
        plot_bgcolor="white",
        yaxis=dict(autorange="reversed"),
        xaxis=dict(title="Antal"),
    )
    return fig


# plot the map on course page
def plot_map(year):
    df_map = map_df(year)
    df_map = df_map.rename(columns={"antal_bev": "Antal beviljade", "code": "Länskod"})
    geo_json = geo_file()
    fig = px.choropleth(
        df_map,
        geojson=geo_json,
        locations="Länskod",
        featureidkey="properties.ref:se:länskod",
        color="Antal beviljade",
        color_continuous_scale="blues",
        hover_name="name",
    )

    fig.update_layout(width=1000, height=700, legend=dict(title="Antal beviljade"))
    fig.update_geos(
        fitbounds="locations", visible=False, projection_type="orthographic"
    )

    return fig
    fig.update_traces(
        hovertemplate="""
            <b>%{hovertext}</b><br>
            Antal invånare: %{antal_bev}<extra></extra>
        """
    )
    return fig


def create_funnel_chart_total(df):
    fig = px.funnel(
        df,
        x="value",
        y="stage",
        title="Utbildningsfunnel: Total antal studenter",
    )
    fig.update_layout(
        plot_bgcolor="white", xaxis_title="Antal personer", yaxis_title="Steg"
    )
    return fig


def create_funnel_chart_gender(df):
    fig = px.funnel(
        df,
        x="number",
        y="stage",
        color="office",
        title="Utbildningsfunnel (Kön)",
    )
    fig.update_layout(
        plot_bgcolor="white", xaxis_title="Antal personer", yaxis_title="Steg"
    )
    return fig


"""def create_funnel_chart_total(df):
    fig = go.Figure(
        go.Funnel(
            y=df["stage"],
            x=df["value"],
            textinfo="value+percent initial",
            marker_color="#4C78A8",
        )
    )

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Antal personer",
        yaxis_title="Steg",
    )
    return fig


def create_funnel_chart_gender(df):
    fig = go.Figure()
    colors = {"Kvinnor": "#EF553B", "Män": "#3B48FD"}

    for office in df["office"].unique():
        office_df = df[df["office"] == office]
        x_values = office_df["number"]
        y_values = office_df["stage"]

        text_positions = ["inside" if x > 2000 else "outside" for x in x_values]

        fig.add_trace(
            go.Funnel(
                name=office,
                y=y_values,
                x=x_values,
                textinfo="value+percent initial",
                textposition=text_positions,
                marker_color=colors.get(office, "#888"),
            )
        )

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Antal personer",
        yaxis_title="Steg",
    )
    return fig"""


# CHARTS AND STATS FOR STORYTELLING PAGE (storytelling 2)


def create_storytelling_chart(df_summary):
    highlight_area = "Ekonomi, administration och försäljning"
    colors = [
        "lightgray" if area != highlight_area else "royalblue"
        for area in df_summary["Utbildningsinriktning"]
    ]

    fig_px = px.bar(
        df_summary,
        y="Utbildningsinriktning",
        x="Antal studerande",
        orientation="h",
        title="Vilket utbildningsområde bör # The Skool fokusera på ?",
        labels={
            "Utbildningsinriktning": "Utbildningsområde",
            "Antal studerande": "Antal studerande",
        },
    )

    fig_px.update_traces(marker_color=colors)
    fig_px.update_layout(
        plot_bgcolor="white",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        margin=dict(l=120, r=80, t=80, b=40),
    )

    if highlight_area in df_summary["Utbildningsinriktning"].values:
        highlight_idx = df_summary.index[
            df_summary["Utbildningsinriktning"] == highlight_area
        ][0]
        highlight_value = df_summary.loc[highlight_idx, "Antal studerande"]

        fig_px.add_annotation(
            x=highlight_value,
            y=highlight_idx - 0.4,
            text=" Viktig tillväxtmöjlighet",
            showarrow=True,
            arrowhead=3,
            arrowcolor="royalblue",
            ax=0,
            ay=30,
            font=dict(color="royalblue", size=13, family="Arial"),
            bgcolor="white",
            bordercolor="royalblue",
            borderwidth=1,
        )

        
    # Konvertera plotly.express-figuren till plotly.graph_objects.Figure
    fig = go.Figure(fig_px)
    return fig
