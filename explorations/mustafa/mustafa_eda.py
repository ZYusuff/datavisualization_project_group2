import pandas as pd
import matplotlib.pyplot as plt
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

def plot_bar(data, title, xlabel, ylabel, filename):
    plt.figure(figsize=(10,6))
    data.sort_values().plot(kind='barh', color='skyblue')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="EDA för beviljade YH-program")
    parser.add_argument('--file', type=str, required=True, help='Sökväg till Excel-fil (.xlsx)')
    args = parser.parse_args()

    if not os.path.exists(args.file):
        raise FileNotFoundError(f"Hittar inte filen: {args.file}")

    df = load_data(args.file)

    print("\n🔟 Topp 10 utbildningsområden:\n")
    top_areas = top_10(df, 'Utbildningsområde')
    print(top_areas)

    print("\n🔟 Topp 10 utbildningsnamn:\n")
    top_names = top_10(df, 'Utbildningsnamn')
    print(top_names)

    print("\n📍 Antal utbildningar per län:\n")
    per_lan = top_10(df, 'Län')
    print(per_lan)

    plot_bar(top_areas, "Top 10 utbildningsområden", "Antal", "Utbildningsområde", "top_utbildningsomraden.png")
    plot_bar(top_names, "Top 10 utbildningsnamn", "Antal", "Utbildningsnamn", "top_utbildningsnamn.png")
    plot_bar(per_lan, "Top 10 län efter antal utbildningar", "Antal", "Län", "top_lan.png")

if __name__ == "__main__":
    main()
