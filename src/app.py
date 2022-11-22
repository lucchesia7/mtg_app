import streamlit as st
from classes.user_functions import User_Functions
from classes.models import dummy_fun

user = User_Functions()


def output():
    # try:
    st.image(user.img_return(card_name))
    img_list = user.recommended_cards(card_name=card_name)
    st.write(
        f"Here are 9 cards that would be recommended for your deck based off {card_name.title()}")
    col1, col2, col3 = st.columns(3)
    col1.image(img_list[0:3])
    col2.image(img_list[4:7])
    col3.image(img_list[8:11])

    # except BaseException:
    #     st.error(f'{card_name.title()} is an invalid card. Please re-try with a valid card name. If the card name is valid, try typing the name exactly as it appears on the card.')


st.title("MTG Tracer")
card_name = st.text_input(
    'Please Input the Full Name of the Card You Would Like to See:')
if st.button('Submit Card'):
    output()
else:
    card_name = 'Sol Ring'
    output()
