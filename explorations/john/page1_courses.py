import pandas as pd
from pathlib import Path
from difflib import get_close_matches

folder_path = Path(__file__).parent
excel_files = list(folder_path.glob("*.xlsx"))

all_data = []
target_columns = ["Diarienummer", "Anordnare namn", "Utbildningsnamn", "Utbildningsområde", "YH-poäng", "Kommun"]

for file_path in excel_files:
    print(f"Processing: {file_path}")
    df = pd.read_excel(file_path, sheet_name=0)
    
    column_mapping = {}
    for target in target_columns:
        best_match = get_close_matches(target, df.columns, n=1)
        #print(best_match)
        if best_match:
            column_mapping[best_match[0]] = target
        #print(column_mapping)
    df_renamed = df.rename(columns=column_mapping)
    relevant_df = df_renamed[target_columns]
    all_data.append(relevant_df)

final_df = pd.concat(all_data, ignore_index=True)
final_df["Diarienummer"] = final_df["Diarienummer"].str[4:8]
final_df = final_df.rename(columns={"Diarienummer": "År"})
print(final_df)

#Lägg till beslut i 2021