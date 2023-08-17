import streamlit as st
import sys
import os
from pathlib import Path

filepath = os.path.join(Path(__file__).parents[1], 'classes')
sys.path.insert(0, filepath)
from user_functions import User_Functions

user = User_Functions()

st.title("Recommended Cards")

card_name = st.text_input(
    'Please Input the Full Name of the Card You Would Like to Find Recommendations for:'
    )
if st.button('Submit Card'):
    # try:
    st.image(user.img_return(card_name))
    img_list = user.recommended_cards(card_name=card_name)
    st.write(
            f"""Here are 9 cards that would be recommended for
            your deck based off {card_name.title()}"""
            )
    col1, col2, col3 = st.columns(3)
    col1.image(img_list[0:3])
    col2.image(img_list[4:7])
    col3.image(img_list[8:11])
    # except BaseException:
    #     st.error(f'''{card_name.title()} is an invalid card. 
    #     Please re-try with a valid card name. If the card name is 
    #     valid, try typing the name exactly as it appears on the card.''')
