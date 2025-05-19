import duckdb
import plotly.express as px
from backend.data_processing.page_1_data_processing import map_df, geo_file

# CHARTS AND STATS FOR THE COURSE PAGE (PAGE 1)
#stats on top of course page
def course_stats(df, **options):
    if "year" in options:
        selected_year = options.get("year")
        total_count = duckdb.query(f"""--sql
                 SELECT COUNT(*) as count
                 FROM df
                WHERE "År" = {selected_year}
        """).df()
        total_count = total_count.iloc[0, 0]
        total_approved = duckdb.query(f"""--sql
                SELECT COUNT(*) as count
                FROM df
                WHERE "År" = {selected_year} AND "Beslut" = 'Beviljad'
        """).df()
        total_approved = total_approved.iloc[0, 0]
        approved_rate = total_approved/total_count
    return (total_count, total_approved, approved_rate)

#table for the course page
def course_school_table(df, school = "", year=2024):
    if school == "":
        df = duckdb.query(f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year}
                GROUP BY skola
                ORDER BY antal_kurser DESC
        """).df()
        return df
    else:
        df = duckdb.query(f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year} AND skola = '{school}'
                GROUP BY skola  
                ORDER BY antal_kurser DESC
        """).df()
        return df
    
#plot the bar chart for area of education
def plot_area(df, year):
        duckdb.register('df_for_query', df)
        plot_df = duckdb.query(f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal
            FROM df
            WHERE "Beslut" = 'Beviljad' AND År = {year}
            GROUP BY Utbildningsområde
                        ORDER BY antal DESC
        """).df()
        fig = px.bar(plot_df, x="antal", y="Utbildningsområde", color="Utbildningsområde", orientation='h')
        fig.update_layout(showlegend=False)
        return fig

#plot the map on course page
def plot_map(year):
    df_map = map_df(year)
    geo_json = geo_file()
    fig = px.choropleth(df_map, 
                        geojson=geo_json, 
                        locations="code", 
                        featureidkey="properties.ref:se:länskod",
                        color="antal_bev",
                        color_continuous_scale="blues",
                        hover_name="name",
                        hover_data=["antal_bev",],
                        )
                        

    fig.update_geos(fitbounds="locations", visible=False, projection_type="orthographic")
    fig.update_layout(width=600)

    fig.update_traces(
        hovertemplate="""
            <b>%{hovertext}</b><br>
            Antal invånare: %{antal_bev}<extra></extra>
        """
    )
    return fig