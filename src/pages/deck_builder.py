import streamlit as st
import pandas as pd
import requests


# Create search form and amount
search_query = st.text_input("Search for a card")
amount = st.number_input('How many would you like to add?', 1, 4)

# Create dataframe object in user-session state
if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame(columns=[
        'name', 'amount', 'set'
    ])


# Define function to search Scryfall API
def search_cards(query):
    params = {"fuzzy": True, 'exact': query}
    r = requests.get("https://api.scryfall.com/cards/named", params=params)
    r = r.json()
    return r


def convert_df():
    return st.session_state['df'].to_csv(index=False, sep = ' ').encode('utf-8')


def print_info():
    st.write(results["mana_cost"])
    st.write(results["type_line"])
    st.write(results['oracle_text'])
    st.write(results['set'].upper())


def reset():
    st.session_state['df'] = pd.DataFrame(columns=[
        'name', 'amount', 'set'
        ])


if st.button('Search'):
    try:
        results = {k: v for k, v in search_cards(search_query).items() if k.startswith(
            tuple(['name', 'mana_cost', 'type_line',
                   'img_uris', 'oracle_text', 'set']))
                   }
    except BaseException:
        st.error(f'''{search_query.title()} is an invalid card. 
        Please re-try with a valid card name. If the card name is 
        valid, try typing the name exactly as it appears on the card.''')
    if results:
        st.session_state.df.loc[len(st.session_state.df)] = [results['name'],
                                                             amount,
                                                             results['set'].upper()]
        st.write(f'The card {results["name"]} has been added to your decklist!')
        st.dataframe(st.session_state.df)
        print(type(st.session_state['df']))
        data = convert_df()
        st.download_button(data=data,
                           label='Download as .txt',
                           file_name='deck_list.txt')
        with st.form('my_form'):
            st.form_submit_button('Clear list?', on_click=reset)
