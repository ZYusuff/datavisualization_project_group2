import taipy.gui.builder as tgb

with tgb.Page() as data_page:
        tgb.navbar()
        tgb.text("## Rådata från Statistiska centralbyrån SCB", mode="md")
        tgb.table(data="{raw_data_table}", page_size=10)