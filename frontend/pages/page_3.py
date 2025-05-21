import taipy.gui.builder as tgb
import plotly.express as px
import pandas as pd

# === Ladda kurs- och programdata ===
kurs_df = pd.read_excel("data/page_3/alla_ansökningar.xlsx")
program_df = pd.read_excel("data/page_3/beviljade_program.xlsx")

# === Förbered kursdata
kurs_df["År"] = kurs_df["Diarienummer"].astype(str).str.extract(r"(\d{4})").astype(int)
kurs_df = kurs_df.rename(columns={
    "Utbildningsanordnare administrativ enhet": "Anordnare",
    "Utbildningsnamn": "Utbildning",
    "Beslut": "Status"
})
kurs_df["Typ"] = "Kurs"

# === Förbered programdata
program_df["År"] = program_df["Diarienummer"].astype(str).str.extract(r"(\d{4})").astype(int)
program_df = program_df.rename(columns={
    "Utbildningsanordnare administrativ enhet": "Anordnare",
    "Utbildningsnamn": "Utbildning"
})
program_df["Status"] = "Beviljad"
program_df["Typ"] = "Program"

# === Slå ihop datan
kolumner = ["Anordnare", "Utbildning", "Status", "År", "Typ"]
df = pd.concat([kurs_df[kolumner], program_df[kolumner]], ignore_index=True)

# === Initiera state-variabler
val_typ = "Kurs"
val_anordnare = ""
val_år = 0
antal_ansökningar = 0
antal_beviljade = 0
beviljandegrad = 0
antal_utbildningar = 0
utbildningstabell = pd.DataFrame(columns=["Utbildning", "Status"])
diagram = px.bar(pd.DataFrame(columns=["Status", "Antal"]), x="Status", y="Antal")

# === Dropdown-listor baserat på val
def get_anordnare_list(typ):
    return sorted(df[df["Typ"] == typ]["Anordnare"].dropna().unique().tolist())

def get_år_list(typ):
    return sorted(df[df["Typ"] == typ]["År"].dropna().unique().tolist())

# === Uppdatera state
def uppdatera_state(state):
    filtered = df[
        (df["Typ"] == state.val_typ) &
        (df["Anordnare"] == state.val_anordnare) &
        (df["År"] == state.val_år)
    ]

    state.antal_ansökningar = len(filtered)
    state.antal_beviljade = len(filtered[filtered["Status"].str.lower() == "beviljad"])
    state.antal_utbildningar = filtered["Utbildning"].nunique()
    state.utbildningstabell = filtered[["Utbildning", "Status"]].sort_values("Utbildning")

    if state.antal_ansökningar > 0:
        state.beviljandegrad = round((state.antal_beviljade / state.antal_ansökningar) * 100, 2)
    else:
        state.beviljandegrad = 0

    status_counts = filtered["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Antal"]

    state.diagram = px.bar(
        status_counts,
        x="Status",
        y="Antal",
        color="Status",
        title="Beviljade vs Ej beviljade",
        color_discrete_sequence=["#2a9d8f", "#e76f51"]
    )

# === GUI
with tgb.Page() as page:
    with tgb.part(class_name="container card"):
        tgb.navbar()

    with tgb.part(class_name="container card stack-large"):
        tgb.text("# Statistik per utbildningsanordnare", mode="md")

        with tgb.layout(columns="1 1 1"):
            tgb.selector("val_typ", lov=["Kurs", "Program"], label="Typ", on_change=uppdatera_state)
            tgb.selector("val_anordnare", lov="{get_anordnare_list(val_typ)}", label="Anordnare", on_change=uppdatera_state)
            tgb.selector("val_år", lov="{get_år_list(val_typ)}", label="År", on_change=uppdatera_state)

        with tgb.layout(columns="1 1 1"):
            with tgb.part(): tgb.text("**Antal ansökningar**"); tgb.text("{antal_ansökningar}")
            with tgb.part(): tgb.text("**Beviljade utbildningar**"); tgb.text("{antal_beviljade}")
            with tgb.part(): tgb.text("**Beviljandegrad**"); tgb.text("{beviljandegrad} %")

        tgb.chart("{diagram}")
        tgb.text("## Utbildningar", mode="md")
        tgb.table("{utbildningstabell}", page_size=10)


