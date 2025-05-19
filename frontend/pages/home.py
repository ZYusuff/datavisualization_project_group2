import taipy.gui.builder as tgb

with tgb.Page() as home_page:
    with tgb.part(class_name="container and card stack-large"):
        tgb.navbar()

        with tgb.part(class_name="max-text-width"):
            tgb.text("#Välkommen till YH dashboard 2024", mode="md")
            tgb.text(
                """ Bla bla bla
            """)