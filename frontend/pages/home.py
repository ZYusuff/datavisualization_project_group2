import taipy.gui.builder as tgb

# from frontend.pages.page_3 import page as page3

with tgb.Page() as home_page:
    with tgb.part(class_name="container and card stack-large"):
        tgb.navbar()

        with tgb.part(class_name="max-text-width"):
            tgb.text("# Välkommen till YH dashboard 2024", mode="md")
            tgb.text(
                """ För att bedriva YH-utbildningar med statligt stöd krävs att varje utbildningsanordnare ansöker om att starta specifika program eller kurser. I ansökningarna måste man visa att utbildningen är förankrad i arbetslivet och att det finns ett faktiskt behov för de kompetenser som utbildningen leder till.

Det är här vårt verktyg kommer in.

På uppdrag av **The Skool** har vi tagit fram en interaktiv dashboard som ger skolledare, utbildningsledare och annan personal en tydlig överblick över ansökningsomgången 2022 - och mycket mer. Med hjälp av insamlade data visualiserar vi statistik, trender och geografi för att skapa förståelse för YH-utbildningarnas omfattning, resultat och effekt över tid.

Initiativet började med ett proof-of-concept från Kokchun, som med sin dashboard väckt nyfikenhet i intervjuer med flera yrkeshögskolor. Med Elvins input från utbildningen i Data Engineering, och erfarna ögon för dataanalys, har vi nu vidareutvecklat idén till ett verktyg som stärker beslutsfattandet och förståelsen för YH-utbildningar nationellt.


## Innehåll

#### COURSES 
- Analysera ansökta och beviljade kurser geografiskt via karta och stapeldiagram.

#### UTBILDNINGSOMRÅDE 
- Följ trender för antal studerande inom olika utbildningsområden år för år.

#### SKOLOR 
- Filtrera fram enskilda anordnare och få fram nyckeltal samt beräkna statsbidrag.

#### Arbetssituation efter YH  
- Utforska vad som händer efter examen – hur många går vidare till arbete?

#### DATA
- Samling av data som visualieringarna är baserade på
                """,
                mode="md",
            )

        # ✅ Lägg till en selector för att visa "Skolor"
        """selected_tab = "Skolor"

        with tgb.part():
            tgb.selector(selected_tab, lov=["Skolor"])

            with tgb.part(render_condition="selected_tab == 'Skolor'"):
                tgb.text(page3)"""
