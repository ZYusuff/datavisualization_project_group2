import pandas as pd
from pathlib import Path

def load_school_data():
    path = Path(__file__).parent.parent.parent / "data/page_3/alla_ansökningar.xlsx"
    df = pd.read_excel(path)

    # Byt till kolumner som finns i din Excel-fil
    df = df.rename(columns={
        "Utbildningsanordnare administrativ enhet": "Anordnare",
        "Utbildningsnamn": "Utbildning",
        "Beslut": "Status"
    })

    # Extrahera år från diarienummer
    df["År"] = df["Diarienummer"].astype(str).str.extract(r"(\d{4})")
    df["År"] = pd.to_numeric(df["År"], errors="coerce")
    df = df.dropna(subset=["År"])
    df["År"] = df["År"].astype(int)

    # Endast nödvändiga kolumner
    return df[["Anordnare", "Utbildning", "Status", "År"]].dropna()
