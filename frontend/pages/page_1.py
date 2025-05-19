import taipy.gui.builder as tgb
from taipy.gui import Gui
import duckdb
import plotly.express as px
import pandas as pd
from pathlib import Path
from difflib import get_close_matches

def course_data_transform():
    folder_path = Path(__file__).parent.parent.parent / "data/page_1"
    excel_files = list(folder_path.glob("*.xlsx"))
    
    all_data = []
    target_columns = ["Diarienummer", "Beslut", "Anordnare namn", "Utbildningsnamn", "Antal beviljade platser", "Utbildningsområde", "YH-poäng", "Kommun"]

    for file_path in excel_files:
        print()
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
    final_df["År"] = final_df["År"].astype(int)
    final_df = final_df.rename(columns={"Utbildningsnamn": "Kursnamn", "Anordnare namn" : "Skola"})
    return final_df

def course_stats(df, **options):
    if "year" in options:
        selected_year = options.get("year")
        total_count = duckdb.query(f"""--sql
                 SELECT COUNT(*) as count
                 FROM df
                WHERE "År" = {selected_year}
        """).df()
        total_count = total_count.iloc[0, 0]
        total_approved = duckdb.query(f"""--sql
                SELECT COUNT(*) as count
                FROM df
                WHERE "År" = {selected_year} AND "Beslut" = 'Beviljad'
        """).df()
        total_approved = total_approved.iloc[0, 0]
        approved_rate = total_approved/total_count
    return (total_count, total_approved, approved_rate)

def course_school(df, school = "", year=2024):
    if school == "":
        df = duckdb.query(f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year}
                GROUP BY skola
                ORDER BY antal_kurser DESC
        """).df()
        return df
    else:
        df = duckdb.query(f"""--sql
                SELECT 
                skola,
                COUNT(kursnamn) AS antal_kurser,
                COUNT(CASE WHEN "Beslut"= 'Beviljad' THEN 1 ELSE NULL END) AS approved_courses,
                approved_courses/ antal_kurser AS rate
                FROM df
                WHERE "År" = {year} AND skola = '{school}'
                GROUP BY skola  
                ORDER BY antal_kurser DESC
        """).df()
        return df

def plot_area(df, year):
        plot_df = duckdb.query(f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal
            FROM df
            WHERE "Beslut" = 'Beviljad' AND År = {year}
            GROUP BY Utbildningsområde
                        ORDER BY antal DESC
        """).df()
        return px.bar(plot_df, x="antal", y="Utbildningsområde", color="Utbildningsområde", orientation='h')

year = 2024
df = course_data_transform()
df_course = course_school(df, school="")
bar_chart = plot_area(df, 2024)
num_courses = course_stats(df, year=2024)[0]
approved_courses = course_stats(df, year=2024)[1]
approved_rate = round(course_stats(df, year=2024)[2]*100,2)

with tgb.Page() as course_page:
    with tgb.part(class_name="container card"):
        tgb.text("# YH Ansökning för kurser {year}", mode= "md")
        tgb.selector(
                    "{year}", 
                    lov=df["År"].unique(), 
                    dropdown=True
                )
        #tgb.part()
        with tgb.part(class_name="container"):
            with tgb.layout(columns="1 1 1"):
                with tgb.part():
                    tgb.text("Sökta kurser")
                    tgb.text("### {num_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljade kurser")
                    tgb.text("### {approved_courses}", mode= "md")
                with tgb.part():
                    tgb.text("Beviljandegrad")
                    tgb.text("### {approved_rate} %", mode= "md")
        tgb.text("## Topp antal beviljade kurser per skola", mode= "md")
        tgb.text("Tabellen är sorterad efter beviljade antal kurser totalt")
        tgb.table("{df_course}", page_size=5)

        tgb.text("## Beviljade kurser per utbildningsområde", mode= "md")
        tgb.chart("{bar_chart}")
        
        tgb.text("# Data", mode="md")
        tgb.table("{df}")


#print(course_stats(course_data_transform(), year= 2022))