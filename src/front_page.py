import os
import streamlit as st
from PIL import Image
from pathlib import Path

filepath = os.path.join(Path(__file__).parents[0], 'data/logo.jpg')
image = Image.open(filepath)
st.title('MTG Tracer')
st.subheader("An app built out of love and passion for Magic")
st.image(image)
st.markdown(""" <style> .font {
font-size:22px ;} 
</style> """, unsafe_allow_html=True)
st.markdown('### **Card Look Up:**'
            '<p class="font">This page searches for an image of an input card, allowing a user to view the card.</p>'
            , unsafe_allow_html=True)
st.markdown('### **Deck Builder:**'
            '''<p class="font">This page will allow you to save cards to a .txt file. This file can be input into Moxfield, MTGA/MTGO, and Forge.</p>''',unsafe_allow_html=True)
st.markdown(
  '''### **Recommended cards:**'''
  '<p class="font">Allows you to input a card name and find cards that are like that are like the input card.'
  , unsafe_allow_html=True)
