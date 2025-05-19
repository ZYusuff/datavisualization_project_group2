import pandas as pd
from utils.constants import DATA_DIRECTORY

def load_and_process_page2_data():
    df_raw = pd.read_excel(DATA_DIRECTORY / "page_2" / "studerande_over_tid.xlsx", header=2)
    df_long = df_raw.melt(
        id_vars=['Unnamed: 0', 'Unnamed: 1', 'Unnamed: 2'],
        var_name='År',
        value_name='Antal studerande'
    )
    df_long.rename(columns={
        'Unnamed: 0': 'Kod',
        'Unnamed: 1': 'Utbildningsinriktning',
        'Unnamed: 2': 'Åldersgrupp'
    }, inplace=True)

    df_long["Antal studerande"] = pd.to_numeric(df_long["Antal studerande"], errors="coerce")
    df_long = df_long.dropna(subset=["Antal studerande"])

    raw_table = df_long[["Utbildningsinriktning", "Åldersgrupp", "År", "Antal studerande"]].copy()

    return df_long, raw_table
