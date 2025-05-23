import taipy.gui.builder as tgb
from backend.data_processing.page_2_data_processing import load_and_process_page2_data
from frontend.charts import create_storytelling_chart


# Ladda och processa data
df_long, _ = load_and_process_page2_data()

# Grupp och summering enligt tidigare
df_summary = df_long.groupby("Utbildningsinriktning", as_index=False)["Antal studerande"].sum()

fig = create_storytelling_chart(df_summary)

with tgb.Page() as storytelling_page:
        tgb.navbar()
        tgb.text("# Storytelling", mode="md")
        tgb.text("### Vi har valt ut ett par visualiseringar att presentera för stakeholders", mode="md")
        #with tgb.part(class_name="card"):
        #    tgb.chart(figure=create_storytelling_chart)
        with tgb.part(class_name="card"):
             tgb.image("assets/figures/education_storytelling2.png", class_name="w100", width=1600, height=1000, scale=2)
