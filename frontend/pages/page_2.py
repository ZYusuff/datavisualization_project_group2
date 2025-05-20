import taipy.gui.builder as tgb
from utils.charts import create_educational_area_bar
import pandas as pd

def page_2(df_long, raw_data_table):
    # Initiera default state
    number_of_years = 20
    selected_educational_area = df_long["Utbildningsinriktning"].dropna().unique()[0]
    educational_area_chart = create_educational_area_bar(df_long, selected_educational_area, number_of_years)
    chart_title = f"Antal studerande de senaste {number_of_years} åren inom {selected_educational_area}"

    # Callback
    def filter_data(state):
        if not state.selected_educational_area or pd.isna(state.selected_educational_area):
            return
        state.educational_area_chart = create_educational_area_bar(
            df_long, state.selected_educational_area, state.number_of_years
        )
        state.chart_title = f"Antal studerande för {state.selected_educational_area}"

    # Skapa sidan
    with tgb.Page() as page_2:
        with tgb.part(class_name="container card"):
            tgb.navbar()
        with tgb.part(class_name="container card stack-large"):
            tgb.text("# MYH Dashboard 2024", mode="md")
            tgb.text(
            "Denna dashboard visar antal studerande inom olika utbildningsområden på yrkeshögskolan (YH) i Sverige över tid. "
            "Data är hämtad från Statistiska centralbyrån (SCB) och omfattar endast YH-utbildningar. "
            "Genom att filtrera på utbildningsinriktning och antal år kan du analysera trender och förändringar i antalet studerande "
            "för att få en översikt över utvecklingen inom olika utbildningsinriktningar.",
            mode="md"
        )

            with tgb.layout(columns="2 1"):
                with tgb.part(class_name="card"):
                    tgb.text("## {chart_title}", mode="md")
                    tgb.chart(figure="{educational_area_chart}")

                with tgb.part(class_name="card left-margin-md"):
                    tgb.text("## Filtrera data", mode="md")
                    tgb.slider("{number_of_years}", min=1, max=20, step=1, continuous=False)
                    tgb.selector(
                        "{selected_educational_area}",
                        lov=df_long["Utbildningsinriktning"].dropna().unique(),
                        dropdown=True,
                    )
                    tgb.button("FILTRERA DATA", class_name="button-color", on_action=filter_data)

    return page_2, {
        "number_of_years": number_of_years,
        "selected_educational_area": selected_educational_area,
        "educational_area_chart": educational_area_chart,
        "chart_title": chart_title,
        "raw_data_table": raw_data_table
    }
