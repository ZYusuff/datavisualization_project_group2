import taipy.gui.builder as tgb
import pandas as pd
import plotly.express as px
from backend.data_processing.page_3_data_processing import load_school_data

# Ladda data
df = load_school_data()
alla_år = sorted(df["År"].unique())
val_år = alla_år[-1]

# Stats- och diagramfunktion
def calculate_state(year):
    filtered = df[df["År"] == year]
    antal_ansökningar = len(filtered)
    antal_beviljade = len(filtered[filtered["Status"] == "Beviljad"])
    beviljandegrad = (
        round(antal_beviljade / antal_ansökningar * 100, 2)
        if antal_ansökningar > 0
        else 0
    )

    # Tabell per skola
    tabell = (
        filtered.groupby(["Anordnare", "Status"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    # Stapeldiagram: antal utbildningar per skola
    bar_data = filtered["Anordnare"].value_counts().reset_index()
    bar_data.columns = ["Anordnare", "Antal utbildningar"]
    bar_data = bar_data.head(15)
    fig = px.bar(
        bar_data,
        x="Anordnare",
        y="Antal utbildningar",
        title=f"Antal utbildningar per anordnare ({year})",
        labels={"Antal utbildningar": "Antal"},
        template="simple_white",
    )

    fig.update_layout(xaxis_tickangle=-45, height=500)

    return antal_ansökningar, antal_beviljade, beviljandegrad, tabell, fig

# Initiera
antal_ansökningar, antal_beviljade, beviljandegrad, skol_tabell, skol_fig = (
    calculate_state(val_år)
)

# Page
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.navbar()

    with tgb.part(class_name="container card"):
        tgb.text(f"# Statistik per Anordnare ({val_år})", mode="md")

        with tgb.layout(columns="1 1 1"):
            with tgb.part():
                tgb.text("Antal ansökningar")
                tgb.text("{antal_ansökningar}")
            with tgb.part():
                tgb.text("Antal beviljade")
                tgb.text("{antal_beviljade}")
            with tgb.part():
                tgb.text("Beviljandegrad")
                tgb.text("{beviljandegrad} %")

        tgb.text(" Topp 15 anordnare med flest utbildningar", mode="md")
        tgb.chart(figure="{skol_fig}")

        tgb.text(f"Tabell över utbildningar ({val_år})", mode="md")
        tgb.table(data="{skol_tabell}", page_size=10)
