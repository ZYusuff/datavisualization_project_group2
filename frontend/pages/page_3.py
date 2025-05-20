import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb

# === Filvägar ===
beviljade_path = "data/page_3/beviljade_program.xlsx"
studerande_path = "data/page_3/studerande_over_tid.xlsx"
beslut_path = "data/page_3/alla_ansökingar.xlsx"

# === Steg 1: Läs in beviljade utbildningar ===
df_beviljade = pd.read_excel(beviljade_path, sheet_name="Tabell 1", skiprows=4)
df_beviljade.columns = [
    "Utbildningsområde", "Utbildningsnamn", "Län", "Kommun", "Diarienummer",
    "Flera kommuner", "Antal kommuner", "YH-poäng", "Utbildningsanordnare"
]
df_beviljade = df_beviljade.dropna(subset=["Utbildningsanordnare"])

summary = (
    df_beviljade.groupby(["Utbildningsanordnare", "Län"])
    .agg(
        antal_program=("Utbildningsnamn", "nunique"),
        antal_kurser=("Utbildningsnamn", "count")
    ).reset_index()
)

områden = (
    df_beviljade.groupby("Utbildningsanordnare")["Utbildningsområde"]
    .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
    .reset_index()
    .rename(columns={"Utbildningsområde": "Område"})
)
summary = summary.merge(områden, on="Utbildningsanordnare", how="left")

# === Steg 2: Studerande ===
df_stud = pd.read_excel(studerande_path)
df_stud_clean = df_stud.iloc[2:, :23].copy()
df_stud_clean.columns = ["Område", "Ålder"] + list(range(2005, 2026))
årskolumner = list(range(2005, 2026))
df_stud_clean[årskolumner] = df_stud_clean[årskolumner].apply(pd.to_numeric, errors="coerce")

df_stud_grouped = (
    df_stud_clean.groupby("Område")[årskolumner]
    .sum()
    .sum(axis=1)
    .reset_index()
    .rename(columns={0: "Antal studerande"})
)
summary = summary.merge(df_stud_grouped, on="Område", how="left")

# === Steg 3: Beviljandegrad ===
df_beslut = pd.read_excel(beslut_path, sheet_name="Tabell 3", skiprows=4)
df_beslut.columns.values[3] = "Utbildningsnamn"
df_beslut.columns.values[4] = "Beslut"
df_beslut.columns.values[27] = "Utbildningsanordnare"

beslut_count = (
    df_beslut.groupby(["Utbildningsanordnare", "Beslut"])
    ["Utbildningsnamn"]
    .count()
    .unstack(fill_value=0)
    .reset_index()
)
beslut_count["Totalt"] = beslut_count.sum(axis=1, numeric_only=True)
beslut_count["Beviljandegrad"] = (beslut_count.get("Beviljad", 0) / beslut_count["Totalt"] * 100).round(1)
summary = summary.merge(
    beslut_count[["Utbildningsanordnare", "Beviljandegrad"]],
    on="Utbildningsanordnare", how="left"
)

# === Steg 4: Topp 5 anordnare ===
top5 = summary.sort_values("antal_kurser", ascending=False).drop_duplicates("Län").head(5)

# === Diagramfunktion ===
def get_bar_chart():
    fig = px.bar(
        top5,
        x="Utbildningsanordnare",
        y=["antal_kurser", "antal_program"],
        barmode="group",
        title="Antal kurser och program per anordnare",
        labels={"value": "Antal", "variable": "Typ"}
    )
    return fig

# === Taipy Page: builder-version ===
with tgb.Page() as page:
    with tgb.part(class_name="card"):
        tgb.text("# 📊 Anordnarstatistik – Topp 5 utbildningsanordnare", mode="md")
        tgb.text(
            """Här visas en översikt av utbildningsanordnare från olika län med flest beviljade kurser.
Tabellen visar antal program, antal kurser, utbildningsområde, antal studerande och beviljandegrad.""",
            mode="md"
        )
        tgb.table(top5)
        tgb.chart(get_bar_chart)

