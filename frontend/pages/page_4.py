import taipy.gui.builder as tgb
from frontend.charts import create_funnel_chart
from backend.data_processing.page_4_data_processing import (
    get_direction_and_year_options,
    prepare_total_data,
)


directions, years = get_direction_and_year_options()
default_direction = "Totalt" if "Totalt" in directions else directions[0]
default_year = max(years)


direction = default_direction
year = default_year

initial_df = prepare_total_data(default_direction, default_year)
funnel_fig = create_funnel_chart(initial_df)


def update_state(state):
    df = prepare_total_data(state.direction, state.year)
    state.funnel_fig = create_funnel_chart(df)


with tgb.Page() as student_page:
    with tgb.part(class_name="container card"):
        tgb.navbar()
        with tgb.part(class_name="container stack-large"):
            tgb.text("# Utbildningsanalys — Funnel chart", mode="md")
            tgb.text(
                "Dynamisk analys av studentflöde: sökande → behöriga → antagna → examinerade. ",
                mode="md",
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
                            label="Year",
                            on_change=update_state,
                        )

            with tgb.part(class_name="card"):
                tgb.text("## Воронка", mode="md")
                tgb.chart(figure="{funnel_fig}")
