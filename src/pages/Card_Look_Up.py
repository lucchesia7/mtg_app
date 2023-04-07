from pathlib import Path

import os
import sys
import streamlit as st

filepath = os.path.join(Path(__file__).parents[1], 'classes')
sys.path.insert(0, filepath)
from user_functions import User_Functions


st.title('Card Look Up')
st.subheader('Enter a card name to look up an image of the card and return information on it.')


user = User_Functions()

search_query = st.text_input("Card Name:")
if st.button('Submit'):
    st.image(user.img_return(search_query))
