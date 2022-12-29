from pathlib import Path
from classes.user_functions import User_Functions
import streamlit as st
import pandas as pd
import os

folder_dir = os.path.join(Path(__file__).parents[1], 'data')
tokens = pd.read_csv(f'{folder_dir}/token_data.csv')

st.title('Token Generator')
st.subheader('Token creation with a counter ability. Input type of token you wish to see')

token_name = st.text_input('Please input the name of the token you wish to create:')
try:
    if token_name:
        st.image(User_Functions.token_generation(token_name, 'tokens'))
    else:
        st.markdown('Please input a token name.')
except:
    st.markdown('Please input a valid token.')
