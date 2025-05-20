import taipy.gui.builder as tgb

with tgb.Page() as data_page:
        tgb.navbar()
        tgb.text("# Rådata", mode="md")
        tgb.text("##### Rådata från Statistiska centralbyrån (SCB) som visar antalet studerande inom olika utbildningsområden på yrkeshögskolan.", mode="md")
        tgb.table(data="{raw_data_table}", page_size=10)