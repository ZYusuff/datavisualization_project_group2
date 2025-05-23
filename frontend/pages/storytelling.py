import taipy.gui.builder as tgb
from backend.data_processing.page_2_data_processing import load_and_process_page2_data
from frontend.charts import create_storytelling_chart
from explorations.john.temp_graph import plot_area_storytelling
from backend.data_processing.page_1_data_processing import course_data_transform


# Ladda och processa data
df_long, _ = load_and_process_page2_data()

# Grupp och summering enligt tidigare
df_summary = df_long.groupby("Utbildningsinriktning", as_index=False)["Antal studerande"].sum()

fig = create_storytelling_chart(df_summary)
bar_chart = plot_area_storytelling(course_data_transform(), 2024)

with tgb.Page() as storytelling_page:
        with tgb.part(class_name="container card"):
                tgb.navbar()
        with tgb.part(class_name="container card"):
                tgb.text("# STIs framtid", mode="md")
                tgb.text("### Den här sidan visar STIs fokusområden och var fokus bör ligga i framtiden", mode="md")
                #with tgb.part(class_name="card"):
                #    tgb.chart(figure=create_storytelling_chart)
        with tgb.part(class_name="container card"):
             tgb.image("assets/figures/education_storytelling2.png", class_name="w100", width=1600, height=1000, scale=2)
        with tgb.part(class_name="container card"):
               tgb.chart(figure="{bar_chart}")