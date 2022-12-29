# import streamlit as st
# import requests


# # Create search form in sidebar
# search_query = st.text_input("Search for a card")

# # Define function to search Scryfall API
# def search_cards(query):
#     params = {"fuzzy": True, 'exact': query}
#     r = requests.get("https://api.scryfall.com/cards/named", params=params)
#     r = r.json()
#     return r

# # Search for cards
# results = search_cards(search_query)

# # Display search results

# st.write(results["name"])
# st.write(results["mana_cost"])
# st.write(results["type_line"])
import sys
sys.path.append(r'C:\Users\Alex Lucchesi\OneDrive\Documents\GitHub\MTG_app\src\classes')
