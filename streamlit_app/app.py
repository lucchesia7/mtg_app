import streamlit as st
from pathlib import Path
import os

from multipage import MultiPage
from pages import (f1)

app = MultiPage()

logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/logo.png')
st.sidebar.image(logo_path, use_column_width=True)
st.title("MillTown")
app.add_page("Home", f1.app)
app.run()