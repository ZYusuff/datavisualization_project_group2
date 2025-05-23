import pandas as pd
from pathlib import Path

_cached_sheets = None


def load_sheet_with_gender(sheet_df):
    df = sheet_df.copy()
    gender = "total"
    gender_col = []

    for _, row in df.iterrows():
        utbildningsområde = row["Utbildningsområde"]
        if utbildningsområde == "Totalt kvinnor":
            gender = "kvinnor"
        elif utbildningsområde == "Totalt män":
            gender = "män"
        elif utbildningsområde == "Totalt":
            gender = "total"
        gender_col.append(gender)

    df["gender"] = gender_col
    df = df[
        ~df["Utbildningsområde"].isin(["Totalt kvinnor", "Totalt män", "Totalt"])
    ].copy()
    return df


"""def load_sheet_with_gender(sheet_df):
    df = sheet_df.copy()
    gender_col = []

    for _, row in df.iterrows():
        utbildningsområde = row["Utbildningsområde"]
        if utbildningsområde == "Totalt kvinnor":
            gender = "kvinnor"
            utbildningsområde = "Totalt"
        elif utbildningsområde == "Totalt män":
            gender = "män"
            utbildningsområde = "Totalt"
        elif utbildningsområde == "Totalt":
            gender = "total"
        else:
            gender = None

        gender_col.append(gender)
        row["Utbildningsområde"] = utbildningsområde

    df["gender"] = gender_col
    return df"""


def load_all_sheets():
    global _cached_sheets
    if _cached_sheets is None:
        path = (
            Path(__file__).parent.parent.parent
            / "data/page_4/sökande_antagna_examinerade_2014_24.xlsx"
        )
        raw_sheets = pd.read_excel(path, skiprows=3, sheet_name=None)
        _cached_sheets = {
            name: load_sheet_with_gender(df) for name, df in raw_sheets.items()
        }
    return _cached_sheets


def find_year_column(df, year):
    year_str = str(year)
    try:
        year_int = int(year)
    except ValueError:
        year_int = None

    if year_str in df.columns:
        return year_str
    elif year_int in df.columns:
        return year_int
    else:
        raise KeyError(f"Year {year} column not found in dataframe columns")


def filter_data_by_direction_and_year(df, direction, year):
    if direction != "Totalt":
        df_filtered = df[df["Utbildningsområde"] == direction]
    else:
        df_filtered = df[df["Utbildningsområde"] == "Totalt"]

    col_name = find_year_column(df_filtered, year)
    result = df_filtered[["Utbildningsområde", col_name, "gender"]].copy()
    result.rename(columns={col_name: "value"}, inplace=True)
    return result


def prepare_gender_comparison_funnel_data(direction, year):
    sheets = load_all_sheets()
    stages = ["sökande", "behöriga", "antagna", "examinerade"]

    data = []

    for stage in stages:
        df = sheets[stage]
        df_filtered = filter_data_by_direction_and_year(df, direction, year)

        for gender_label in ["kvinnor", "män"]:
            df_gender = df_filtered[df_filtered["gender"] == gender_label]
            if not df_gender.empty:
                value = df_gender["value"].values[0]
            else:
                value = 0

            data.append(
                {
                    "number": value,
                    "stage": stage,
                    "office": "Kvinnor" if gender_label == "kvinnor" else "Män",
                }
            )

    return pd.DataFrame(data)


def prepare_total_data(direction, year):
    sheets = load_all_sheets()
    stages = ["sökande", "behöriga", "antagna", "examinerade"]
    funnel_data = []

    for stage in stages:
        df = sheets[stage]
        filtered = filter_data_by_direction_and_year(df, direction, year)

        filtered = filtered[filtered["gender"] == "total"]

        if not filtered.empty:
            val = filtered["value"].values[0]
            funnel_data.append({"stage": stage, "value": val})
        else:
            funnel_data.append({"stage": stage, "value": 0})

    return pd.DataFrame(funnel_data)


def get_direction_and_year_options():
    sheets = load_all_sheets()
    df_sokande = sheets["sökande"]

    directions = df_sokande["Utbildningsområde"].unique().tolist()

    years = []
    for col in df_sokande.columns:
        if col not in ["Utbildningsområde", "gender"]:
            try:
                years.append(int(col))
            except ValueError:
                pass
    years.sort()

    return directions, years


"""def get_direction_and_year_options():
    sheets = load_all_sheets()
    df_sokande = sheets["sökande"]

    directions = df_sokande["Utbildningsområde"].unique().tolist()
    if "Totalt" not in directions:
        directions.append("Totalt")
    directions = sorted(set(directions))

    years = []
    for col in df_sokande.columns:
        if col not in ["Utbildningsområde", "gender"]:
            try:
                years.append(int(col))
            except ValueError:
                pass
    years.sort()

    return directions, years"""
