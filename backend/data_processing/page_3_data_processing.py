import pandas as pd
from utils.constants import DATA_DIRECTORY

def load_school_data():
    file_path = DATA_DIRECTORY / "page_3" / "alla_ansökningar.xlsx"
    df = pd.read_excel(file_path)

    # Byt till standardiserade kolumnnamn
    df = df.rename(columns={
        "Utbildningsnamn": "Utbildning",
        "Utbildningsanordnare administrativ enhet": "Anordnare",
        "Beslut": "Status",
        "Diarienummer": "Diarienummer"
    })

    # Extrahera år från diarienummer
    df["År"] = df["Diarienummer"].astype(str).str.extract(r"(\d{4})")
    df = df.dropna(subset=["År"])
    df["År"] = df["År"].astype(int)

    # Behåll endast relevanta kolumner
    df = df[["Anordnare", "Utbildning", "Status", "År"]].dropna()
    df["Status"] = df["Status"].str.strip().str.capitalize()

    return df
