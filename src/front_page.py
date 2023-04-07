import os
import streamlit as st
from PIL import Image
from pathlib import Path

filepath = os.path.join(Path(__file__).parents[0], 'data\logo.jpg')
image = Image.open(filepath)
st.title('MTG Tracer')
st.subheader("An app built out of love and passion for Magic")
st.image(image)
st.text('''
• Deck Builder will allow you to save cards to a list.
  This list can be input into Moxfield, MTGA/MTGO, and Forge.
• Recommended cards allows you to input a card name and find 
  cards that are like that are like the input card. 


Please click on the page you wish to use.
                ''')