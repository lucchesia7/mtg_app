import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import os
from classes.user_functions import User_Functions

st.title("Magic the Gathering Card Viewer and Recommendation System")

card_name = st.text_input('Please Input the Full Name of the Card you Would Like to See:')

try:
  st.image(User_Functions().img_return(card_name.lower()))
  st.write(f"Here are 10 cards that would be recommended for your deck based off {card_name.title()}")
  st.image(User_Functions().recommended_cards(card_name = card_name))
except:
  pass
