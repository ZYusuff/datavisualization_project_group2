import taipy.gui.builder as tgb
from taipy.gui import Gui
import duckdb
import plotly.express as px
import pandas as pd
from pathlib import Path
from difflib import get_close_matches
from backend.data_processing.page_1_data_processing import map_df, geo_file, course_data_transform
from frontend.charts import course_stats, course_school_table, plot_area, plot_map

def update_state(state):
    #the 3 stats
    state.num_courses = course_stats(df, year=state.year)[0]
    state.approved_courses = course_stats(df, year=state.year)[1]
    state.approved_rate = round(course_stats(df, year=state.year)[2]*100,2)
    state.df_course = course_school_table(df, year=state.year)
    state.fig = plot_area(df, year=state.year)
    state.fig2 = plot_map(year=state.year)
    

year = 2024
df = course_data_transform()
df_course = course_school_table(df, school="", year=year)
num_courses = course_stats(df, year=year)[0]
approved_courses = course_stats(df, year=year)[1]
approved_rate = round(course_stats(df, year=year)[2]*100,2)
fig = plot_area(df, year=year)
fig2 = plot_map(year=year)

with tgb.Page() as course_page:
    with tgb.part(class_name="container card"):
        tgb.navbar()
    with tgb.part(class_name="container card"):
        tgb.text("# YH Ansökning för kurser {year}", mode= "md")
        tgb.selector(
                    "{year}", 
                    lov=df["År"].unique(), 
                    dropdown=True,
                    on_change=update_state
                )
        with tgb.part(class_name="container"):
            with tgb.layout(columns="1 1 1"):
                with tgb.part():
                    tgb.text("Sökta kurser")
                    tgb.text("### {num_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljade kurser")
                    tgb.text("### {approved_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljandegrad")
                    tgb.text("### {approved_rate} %", mode= "md")
        tgb.text("## Topp antal beviljade kurser per skola, {year}", mode= "md")
        tgb.text("Tabellen är sorterad efter beviljade antal kurser totalt")
        tgb.table("{df_course}", page_size=5)

        tgb.text("## Beviljade kurser per utbildningsområde, {year}", mode= "md")
        tgb.chart(figure="{fig}")

        tgb.text("## Beviljade kurser per region, {year}", mode= "md")
        tgb.chart(figure="{fig2}")

        tgb.text("# Data", mode="md")
        tgb.table("{df}")