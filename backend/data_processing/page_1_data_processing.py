import json
from pathlib import Path
import pandas as pd
from difflib import get_close_matches
import duckdb

def course_data_transform():
    folder_path = Path(__file__).parent.parent.parent / "data/page_1"
    excel_files = list(folder_path.glob("*.xlsx"))
    
    all_data = []
    target_columns = ["Diarienummer", "Beslut", "Anordnare namn", "Utbildningsnamn", "Antal beviljade platser", "Utbildningsområde", "YH-poäng", "Kommun", "Antal beviljade platser", "Antal kommuner", "Län"]

    for file_path in excel_files:
        #print(f"Processing: {file_path}")
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
    final_df["År"] = final_df["År"].astype(int)
    final_df = final_df.rename(columns={"Utbildningsnamn": "Kursnamn", "Anordnare namn" : "Skola"})
    return final_df
#print(course_data_transform().columns)

def approved_courses():
    df = course_data_transform()
    approved_courses = duckdb.query(f"""--sql
        SELECT
            all_combs.län,
            all_combs.År,
            COALESCE(actual_counts.antal_bev, 0) AS antal_bev
        FROM
            (SELECT DISTINCT län, År
            FROM df) AS all_combs
        LEFT JOIN
        (SELECT
            län,
            År,
            COUNT(beslut) AS antal_bev
        FROM
            df
        WHERE
            "Antal kommuner" <= 1 AND Beslut = 'Beviljad'
        GROUP BY
            län, År) AS actual_counts
    ON
        all_combs.län = actual_counts.län AND all_combs.År = actual_counts.År
    ORDER BY
        antal_bev DESC, all_combs.År;
    """).df()
    return approved_courses

def geo_file():
    geo_path = Path(__file__).parent.parent.parent/ "data/page_1"
    with open(geo_path/"swedish_regions.geojson") as map_file:
        geo_regions = json.load(map_file)
        return geo_regions


def regions_df():
    geo_regions = geo_file()
    regions_list = []
    for geo in geo_regions.get("features", []):
        region_data = {
            "name": geo["properties"].get("name"),
            "code": geo["properties"].get("ref:se:länskod")
        }
        regions_list.append(region_data)

    df_regions = pd.DataFrame(regions_list)
    df_regions["name"] = df_regions["name"]

    name_mapping = {}
    appr_course = approved_courses()
    for name in df_regions['name']:
        best_match = get_close_matches(name, appr_course["Län"], n=1)
        if name == "Gotlands län":
            best_match = ["Gotland"]
        if best_match:
            name_mapping[name] = best_match[0]
        df_regions['matched_name'] = df_regions['name'].map(name_mapping)
    return df_regions

def map_df(year = 2022):
    appr_course = approved_courses()
    regions = regions_df()
    map_df = duckdb.query(f"""--sql
             SELECT r.name, code, antal_bev, a.År
             FROM regions as r
                    FULL JOIN appr_course as a
                    ON a.län = r.matched_name
                    WHERE a.År = {year}
                    ORDER BY antal_bev DESC
    """).df()

    map_df = map_df.fillna(0)
    map_df["antal_bev"] = map_df["antal_bev"].astype(int)

    return map_df

def scrape_revenue():
    revenue_df = pd.read_html("https://www.myh.se/yrkeshogskolan/ansok-om-att-bedriva-utbildning/ansokan-kurser/statsbidrag-och-schablonnivaer", encoding='utf-8')[0]
    revenue_df["Med momskompensation"]=revenue_df["Med momskompensation"].str.replace(" ", "").astype(int)
    revenue_df["Utan momskompensation"]=revenue_df["Utan momskompensation"].str.replace(" ", "").astype(int)
    return revenue_df


def available_money(year):
    df = course_data_transform()
    df_money=scrape_revenue()
    rev_df = duckdb.query("""--sql
            WITH CTE as (
            SELECT skola, f.Utbildningsområde, År, SUM("Antal beviljade platser") as bev_platser, m."Med momskompensation" as komp
             FROM df as f
               LEFT JOIN df_money as m
                   ON f.Utbildningsområde = m.Utbildningsområde
                   where beslut = 'Beviljad'
                   group by skola, f.Utbildningsområde, "År", m."Med momskompensation"
                      )
               SELECT skola, År, SUM(bev_platser*komp) as tot_rev
                 FROM CTE
                   GROUP BY skola, "År"
                   ORDER BY tot_rev DESC
    """).df()
    rev_df = rev_df.rename(columns={"skola":"Skola"})
    rev_df = rev_df.query(f'År=={year}')
    #rev_df["tot_rev"] = rev_df["tot_rev"].apply(lambda x: f'{x:,}')
    return rev_df


def table_formatter(year):
    df= available_money(year)
    df["tot_rev"] = df["tot_rev"].apply(lambda x: f'{x:,}')
    return df