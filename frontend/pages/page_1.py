import taipy.gui.builder as tgb
from taipy.gui import Gui
import plotly.express as px
import pandas as pd
from backend.data_processing.page_1_data_processing import course_data_transform, available_money, table_formatter
from frontend.charts import course_stats, course_school_table, plot_area, plot_map

def update_state(state):
    #the 3 stats
    state.num_courses = course_stats(df, year=state.year)[0]
    state.approved_courses = course_stats(df, year=state.year)[1]
    state.approved_rate = round(course_stats(df, year=state.year)[2]*100,2)
    state.df_course = course_school_table(df, year=state.year)
    state.fig = plot_area(df, year=state.year)
    state.fig2 = plot_map(year=state.year)
    state.tot_rev = round(available_money(state.year)["tot_rev"].sum()/1000000000,3)
    state.df_course = course_school_table(df, school="", year=state.year)
    state.df_money = table_formatter(state.year).rename(columns={"tot_rev":"Beviljat statsbidrag"})
    state.df_course_display = pd.merge(state.df_course, state.df_money, on='Skola', how='left')[["Skola", "Antal kurser", "Beviljade kurser", "Beviljandegrad", "Beviljat statsbidrag (SEK)"]]
    
    

year = 2024
df = course_data_transform()
df_course = course_school_table(df, school="", year=year)
df_money = table_formatter(year).rename(columns={"tot_rev":"Beviljat statsbidrag (SEK)"})
df_course_display = pd.merge(df_course, df_money, on='Skola', how='left')[["Skola", "Antal kurser", "Beviljade kurser", "Beviljandegrad", "Beviljat statsbidrag (SEK)"]]
num_courses = course_stats(df, year=year)[0]
approved_courses = course_stats(df, year=year)[1]
approved_rate = round(course_stats(df, year=year)[2]*100,2)
fig = plot_area(df, year=year)
fig2 = plot_map(year=year)
tot_rev = round(available_money(year)["tot_rev"].sum()/1000000000,3)

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
            with tgb.layout(columns="1 1 1 1"):
                with tgb.part():
                    tgb.text("Sökta kurser")
                    tgb.text("### {num_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljade kurser")
                    tgb.text("### {approved_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljandegrad")
                    tgb.text("### {approved_rate} %", mode= "md")
                with tgb.part():
                    tgb.text("Totalt tillgängligt statsbidrag")
                    tgb.text("### {tot_rev} md SEK", mode= "md")
        tgb.text("## Topp antal beviljade kurser per skola, {year}", mode= "md")
        tgb.text("Tabellen är sorterad efter beviljade antal kurser totalt")
        tgb.table("{df_course_display}", page_size=5)

        tgb.text("## Beviljade kurser per utbildningsområde, {year}", mode= "md")
        tgb.chart(figure="{fig}")

        tgb.text("## Beviljade kurser per region, {year}", mode= "md")
        tgb.chart(figure="{fig2}")