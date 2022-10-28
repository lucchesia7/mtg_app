import streamlit as st
from classes.user_functions import User_Functions
user = User_Functions()
st.title("MTG Tracer")
# card_name = st.selectbox(f'Please Input the Full Name of the Card you Would Like to See:', options=('', user.df['name']))
card_name = st.text_input('Please Input the Full Name of the Card You Would Like to See:')
if st.button('Submit Card'):
    try:
        st.image(user.img_return(card_name.title()))
        img_list = user.recommended_cards(card_name = card_name)
        st.write(f"Here are {len(img_list)} cards that would be recommended for your deck based off {card_name.title()}")
        col1, col2, col3 = st.columns(3)
        col1.image(img_list[0:3])
        col2.image(img_list[4:7])
        col3.image(img_list[8:11])
        
    except:
        st.error(f'{card_name.title()} is an invalid card. Please re-try with a valid card name. If the card name is valid, try typing the name exactly as it appears on the card.')
else:
    pass
      
