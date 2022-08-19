import streamlit as st
from classes.user_functions import User_Functions
user = User_Functions()
st.title("Magic the Gathering Card Viewer and Recommendation System")
# card_name = st.selectbox(f'Please Input the Full Name of the Card you Would Like to See:', options=('', user.df['name']))
card_name = st.text_input('Please Input the Full Name of the Card you Would Like to See:')
if st.button('Submit Card'):
      try:
        st.image(user.img_return(card_name.lower()))
        st.write(f"Here are 10 cards that would be recommended for your deck based off {card_name.title()}")
        img_list = user.recommended_cards(card_name = card_name)
        col1, col2 = st.columns(2)
        n = len(img_list) // 2
        col1.image(img_list[:n])
        col2.image(img_list[n:])
      except:
        st.error(f'{card_name.title()} is an invalid card. Please re-try with a valid card name')
else:
      pass
      
