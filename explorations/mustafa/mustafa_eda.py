

import pandas as pd
import plotly.express as px
import argparse
import os

def load_data(filepath):
    df = pd.read_excel(filepath, sheet_name="Tabell 1", skiprows=5, engine='openpyxl')
    df.columns = df.columns.str.strip()
    print("Kolumner i filen:", df.columns.tolist())

    expected_columns = ['Utbildningsnamn', 'Utbildningsområde', 'Län']
    for col in expected_columns:
        if col not in df.columns:
            raise KeyError(f"Kolumn '{col}' hittades inte i Excel-filen.")
    df = df.dropna(subset=expected_columns)
    return df

def top_10(df, column):
    return df[column].value_counts().head(10)

# stapeldiagram
def plot_bar(data, title, xlabel, ylabel, outfile=None):
    fig = px.bar(
        data.sort_values(),
        orientation='h',
        labels={"value": xlabel, "index": ylabel},
        title=title
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    if outfile:
        fig.write_image(outfile)  
    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Interaktiv EDA med Plotly för beviljade YH-program")
    parser.add_argument('--file', type=str, required=True, help='Sökväg till Excel-filen (t.ex. beviljade_program.xlsx)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"Filen hittades inte: {args.file}")

    print("Läser in data...")
    df = load_data(args.file)

    print("\n🔟 Topp 10 utbildningsområden:\n")
    top_areas = top_10(df, 'Utbildningsområde')
    print(top_areas)
    plot_bar(top_areas, "Top 10 utbildningsområden", "Antal", "Utbildningsområde", "top_utbildningsomraden.png")

    print("\n🔟 Topp 10 utbildningsnamn:\n")
    top_names = top_10(df, 'Utbildningsnamn')
    print(top_names)
    plot_bar(top_names, "Top 10 utbildningsnamn", "Antal", "Utbildningsnamn", "top_utbildningsnamn.png")

    print("\n📍 Antal utbildningar per län:\n")
    top_lan = top_10(df, 'Län')
    print(top_lan)
    plot_bar(top_lan, "Top 10 län efter antal utbildningar", "Antal", "Län", "top_lan.png")

if __name__ == "__main__":
    main()
