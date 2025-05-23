from taipy.gui import Gui
from backend.data_processing.page_2_data_processing import load_and_process_page2_data
from frontend.pages.page_1 import course_page
from frontend.pages.page_2 import page_2
from frontend.pages.page_3 import page as page_3
from frontend.pages.home import home_page
from frontend.pages.data import data_page
from frontend.pages.page_4 import student_page
from frontend.pages.storytelling import storytelling_page

# Ladda data globalt
df_long, raw_data_table = load_and_process_page2_data()

# Anropa funktionen för att få sidan och initial state
page2_page, page2_state = page_2(df_long, raw_data_table)


pages = {
    "home": home_page,
    "Courses": course_page,
    "utbildningsområde": page2_page,
    "Skolor": page_3,
    "students": student_page,
    "data": data_page,
    "data": data_page,
    "Storytelling": storytelling_page,
}

Gui(pages=pages, css_file="assets/main.css").run(
    dark_mode=False, use_reloader=True, port="8080"
)
