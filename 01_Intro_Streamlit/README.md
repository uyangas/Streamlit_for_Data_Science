# Intro to Streamlit

1. Апп үүсгэх, уншуулах
    - `streamlit run app.py`
1. `config.toml` файлд өөрчлөлт оруулах
    - `streamlit config show`
    - `code ~/.streamlit/config.toml`
    - `touch ~/.streamlit/config.toml`
1. Хуудасны тохиргоо хийх
    - `st.set_page_config()`
        - `page_title`: Sets the title of the Streamlit app displayed in the browser tab
        - `page_icon`: Sets the favicon of the Streamlit app displayed in the browser tab
        - `layout`: Sets the initial state of the sidebar `"wide", "centered"`
        - `initial_sidebar_state`: Sets the initial state of the sidebar. `"auto", "expanded", "collapsed"`
        - `menu_items`: A dictionary of menu items to be displayed in the app sidebar. The keys are the labels, and the values are functions to be called when the item is clicked
