import taipy.gui.builder as tgb
from backend.data_processing.page_1_data_processing import course_data_transform

course_df = course_data_transform()

with tgb.Page() as data_page:
        with tgb.part(class_name="container card"):
                tgb.navbar()
        with tgb.part(class_name="container"):
                tgb.text("## Rådata från Statistiska centralbyrån SCB som visar antal studerande i olika utbildningsområden genom åren", mode="md")
                tgb.table(data="{raw_data_table}", page_size=10)
        with tgb.part(class_name="container"):
                tgb.text("## Rådata ansökningsomgång kurser", mode="md")
                tgb.table(data="{course_df}", page_size=10)
