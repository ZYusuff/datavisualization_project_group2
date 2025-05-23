# Med 2 charts
"""import taipy.gui.builder as tgb
from taipy.gui import Gui
import plotly.express as px
import pandas as pd
from frontend.charts import create_funnel_chart_total, create_funnel_chart_gender
from backend.data_processing.page_4_data_processing import (
    get_direction_and_year_options,
    prepare_total_data,
    prepare_gender_comparison_funnel_data,
)


directions, years = get_direction_and_year_options()
default_direction = "Totalt" if "Totalt" in directions else directions[0]
default_year = max(years)


direction = default_direction
year = default_year

initial_total_df = prepare_total_data(default_direction, default_year)
initial_gender_df = prepare_gender_comparison_funnel_data(
    default_direction, default_year
)

funnel_fig = create_funnel_chart_total(initial_total_df)
gender_funnel_fig = create_funnel_chart_gender(initial_gender_df)


def update_state(state):
    state.funnel_fig = create_funnel_chart_total(
        prepare_total_data(state.direction, state.year)
    )
    state.gender_funnel_fig = create_funnel_chart_gender(
        prepare_gender_comparison_funnel_data(state.direction, state.year)
    )


with tgb.Page() as student_page:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="container stack-large"):
            tgb.text("# Utbildningsanalys — Funnel chart", mode="md")
            tgb.text(
                "Dynamisk analys av studentflöde: *sökande → behöriga → antagna → examinerade*. ",
                mode="md",
                class_name="h4",
            )

        with tgb.part(class_name="container stack-large"):
            with tgb.part():
                tgb.text("### Filter", mode="md")

                with tgb.layout(columns="1 1"):
                    with tgb.part():
                        tgb.selector(
                            "{direction}",
                            lov=directions,
                            dropdown=True,
                            label="Utbildningsområde",
                            on_change=update_state,
                        )

                    with tgb.part():
                        tgb.selector(
                            "{year}",
                            lov=years,
                            dropdown=True,
                            label="År",
                            on_change=update_state,
                        )
            with tgb.layout(columns="1 1"):
                with tgb.part(class_name="card"):
                    tgb.text("## Total (alla studenter)", mode="md")
                    tgb.chart(figure="{funnel_fig}")

                with tgb.part(class_name="card"):
                    tgb.text("## Jämförelse: Kvinnor vs Män", mode="md")
                    tgb.chart(figure="{gender_funnel_fig}")"""


import taipy.gui.builder as tgb
from taipy.gui import Gui
import plotly.express as px
import pandas as pd
from frontend.charts import create_funnel_chart_total, create_funnel_chart_gender
from backend.data_processing.page_4_data_processing import (
    get_direction_and_year_options,
    prepare_total_data,
    prepare_gender_comparison_funnel_data,
)


directions, years = get_direction_and_year_options()
default_direction = "Totalt" if "Totalt" in directions else directions[0]
default_year = max(years)
default_view = "Totalt"


direction = default_direction
year = default_year
funnel_view = default_view


initial_df = prepare_total_data(direction, year)
funnel_fig = create_funnel_chart_total(initial_df)


def update_state(state):
    if state.funnel_view == "Totalt":
        df = prepare_total_data(state.direction, state.year)
        state.funnel_fig = create_funnel_chart_total(df)
    elif state.funnel_view == "Kön":
        df = prepare_gender_comparison_funnel_data(state.direction, state.year)
        state.funnel_fig = create_funnel_chart_gender(df)


with tgb.Page() as student_page:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="container stack-large"):
            tgb.text("# Utbildningsanalys — Funnel chart", mode="md")
            tgb.text(
                "Dynamisk analys av studentflöde: *sökande → behöriga → antagna → examinerade*.",
                mode="md",
                class_name="h4",
            )

        with tgb.part(class_name="container stack-large"):
            with tgb.part():

                with tgb.part(class_name="container"):
                    with tgb.layout(columns="1 1 1 1"):
                        with tgb.part():
                            tgb.text("Sökande")
                            tgb.text("### 12000", mode="md")
                        with tgb.part():
                            tgb.text("Behöriga")
                            tgb.text("### 9000", mode="md")
                        with tgb.part():
                            tgb.text("Antagna")
                            tgb.text("### 6000", mode="md")
                        with tgb.part():
                            tgb.text("Examinerade")
                            tgb.text("### 3000", mode="md")

                with tgb.layout(columns="1 1 1"):
                    with tgb.part():
                        tgb.selector(
                            "{direction}",
                            lov=directions,
                            dropdown=True,
                            label="Utbildningsområde",
                            on_change=update_state,
                        )
                    with tgb.part():
                        tgb.selector(
                            "{year}",
                            lov=years,
                            dropdown=True,
                            label="År",
                            on_change=update_state,
                        )
                    with tgb.part():
                        tgb.selector(
                            "{funnel_view}",
                            lov=["Totalt", "Kön"],
                            dropdown=True,
                            label="Visa som",
                            radio=True,
                            multiple=False,
                            on_change=update_state,
                        )

            with tgb.part(class_name="card"):
                tgb.text("## Visualisering", mode="md")
                tgb.chart(figure="{funnel_fig}")
