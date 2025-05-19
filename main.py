from taipy.gui import Gui
from backend.data_processing.page_2_data_processing import load_and_process_page2_data
from frontend.pages.page_2 import build_page

# Ladda data
df_long, raw_data_table = load_and_process_page2_data()

# Bygg sidan och init-state
page, initial_state = build_page(df_long, raw_data_table)

if __name__ == "__main__":
    Gui(page, css_file="assets/main.css").run(dark_mode=False, use_reloader=True, port="auto")