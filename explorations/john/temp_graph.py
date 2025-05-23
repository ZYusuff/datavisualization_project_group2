import duckdb
import plotly.express as px

def plot_area_storytelling(df, year=2024):
        duckdb.register('df_for_query', df)
        plot_df = duckdb.query(f"""--sql
            SELECT Utbildningsområde, COUNT(*) as antal, Beslut
            FROM df
            WHERE År = {year}
            GROUP BY Utbildningsområde, Beslut
                        ORDER BY antal DESC
        """).df()

        bar_colors = {
            'Beviljad': '#084083',
            'Avslag': '#E4ECF6',
        }

        unique_utbildningsomrade = plot_df['Utbildningsområde'].unique().tolist()
        tick_vals = list(range(len(unique_utbildningsomrade)))
        tick_texts = []
        for category in unique_utbildningsomrade:
            if category == 'Data/IT':
                 tick_texts.append(f"<span style='color:black; font-weight: bold; font-size: 1.1em;'>{category}</span>")
            elif category == 'Samhällsbyggnad och byggteknik':
                 tick_texts.append(f"<span style='color:black; font-weight: bold; font-size: 1.1em;'>{category}</span>")
            else:
                tick_texts.append(f"<span style='color:#a9a9a9'>{category}</span>")


        fig = px.bar(plot_df, 
                     x="antal", 
                     y="Utbildningsområde", 
                     color="Beslut", 
                     color_discrete_map = bar_colors,
                     orientation='h', 
                     text_auto=True,
                     height=800,
                     title= r"Stor skillnad i beviljandegrad för STIs huvudområden. Data/IT<br>har både mer sökta kurser och majoriteten avslagna")
        fig.update_layout(
            showlegend=False, 
            barmode='group',
            plot_bgcolor="white",
            yaxis=dict(
              autorange="reversed",
              title="",
              tickmode='array',
              tickvals=tick_vals,
              ticktext=tick_texts
            ),
            xaxis=dict(
                  title=r"<b>ANTAL</b>"),
            title=dict(font=dict(size=24), x=0.1, y=0.925),
            margin=dict(l=0,t=150)
            )
        
        fig.add_annotation(
            text=r"<b>UTBILDNINGSOMRÅDE</b>",
            yref='paper', xref='paper',
            x=-0.27, y=1.04,
            showarrow=False,
            align='right',
            font=dict(size=14)
        )

        fig.add_annotation(
            text=r"Utbildningsområde med<br><b>hög</b> beviljandegrad",
            yref='paper', xref='paper',
            x=0.595, y=0.72, #position
            showarrow=True,
            # --- Arrowhead ---
            ax=30, # X-koordinater var pilen pekar
            ay=60, # Y-koord
            axref='pixel', #'ax' som värde på x-axeln
            ayref='pixel',
            arrowhead=5,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='black',
            standoff=1,
            startstandoff=1,
            align='left',
            font=dict(size=10)
        )
        fig.add_annotation(
            text=r"Utbildningsområde med<br><b>låg</b> beviljandegrad",
            yref='paper', xref='paper',
            x=0.7, y=0.89,
            ax=30, 
            showarrow=True,
            ay=60, 
            axref='pixel',
            arrowhead=5, 
            ayref='pixel',
            arrowsize=1,
            arrowwidth=2,
            arrowcolor='black',
            standoff=1,
            startstandoff=1,
            align='left',
            font=dict(size=10)
        )
        fig.add_annotation(
            text=r"Data från ansökningsomgång myh kurser 2024",
            yref='paper', xref='paper',
            x=0.88, y=0.05,
            showarrow=False,
            align='left',
            font=dict(size=12, color='#a9a9a9'))
        
        fig.add_layout_image(
        dict(
            source="download.jpeg",
            xref="paper",
            yref="paper",
            x=0.98,
            y=0.03,
            sizex=0.15,
            sizey=0.15,
            )
    )
        fig.write_html("storytelling_course.html")
        return fig