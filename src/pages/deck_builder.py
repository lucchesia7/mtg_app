import streamlit as st
import pandas as pd
import requests


# # Create search form in sidebar
search_query = st.text_input("Search for a card")
amount = st.number_input('How many would you like to add?', 1, 4)
df = pd.DataFrame(columns=['name', 'amount', 'set'])


# # Define function to search Scryfall API
def search_cards(query):
    params = {"fuzzy": True, 'exact': query}
    r = requests.get("https://api.scryfall.com/cards/named", params=params)
    r = r.json()
    return r


def print_card_info():
    st.write(results["mana_cost"])
    st.write(results["type_line"])
    st.write(results['oracle_text'])
    st.write(results['set'].upper())


# # Search for cards
results = {k: v for k, v in search_cards(search_query).items() if k.startswith(
    tuple(['name', 'mana_cost', 'type_line',
           'img_uris', 'oracle_text', 'set']))
           }

if search_query:
    df.append([results['name'], amount, results['set'].upper()], ignore_index=True)
    st.write(f'The card {results["name"]} has been added to your decklist!')
    with st.form(key='my_form'):
        st.write(df)
        if st.button('View More Info',
                    help='Click here if you want to see more information about the card you added'):
            print_card_info()
