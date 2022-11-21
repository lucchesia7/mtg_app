import spacy
import numpy as np
import pandas as pd
import os

from pathlib import Path
import re
import warnings
from pathlib import Path
from .base import Data_Scraping
warnings.filterwarnings("ignore")

"""
Some Key notes:

uri points you to the individual json object where you can locate all info on the data
download_uri points you to the actual json data for the cards.

Included Functions:

cleaning_scryfall_data: Reads in dataframe from base.py and cleans it. Focuses on if statements, to allow flexibility in use.
Input on this is fixed, but allows users to change the direction of the call so it can call to other sites as well as other frames provided by scryfall.

modeling_prep_mtg_oracle: Performs basic modeling preparation for the scryfall dataset. Goal is to create a recommendation model for users to build decks.
"""

filepath = os.path.join(Path(__file__).parents[1], 'data/oracle_data.csv')


class Data_Handling(Data_Scraping):
    def __init__(self):
        super().__init__()

    def cleaning_scryfall_data(self, n: str = 'oracle_cards'):
        '''
        Input: string with name of database we are trying to access
        Output: cleaned data for mtg cards.
        '''
        self.df = super().get_data_with(n=n)

        if 'edhrec_rank' in self.df.columns:
            edh_fix = self.df[self.df['edhrec_rank'].isna()]
            counter = 22665  # Max rank + 1

            edh_fix.edhrec_rank = range(counter, (counter + len(edh_fix)))
            self.df.loc[edh_fix.index, :] = edh_fix[:]
            self.df['edhrec_rank'] = self.df['edhrec_rank'].astype('int64')

        # Fix power column
        if 'power' in self.df.columns:
            self.df['power'].loc[self.df['power'].isna()] = 0

        # Fix Toughness Columns
        if 'toughness' in self.df.columns:
            self.df['toughness'].loc[self.df['toughness'].isna()] = 0

        # Fix CMC Column
        if 'cmc' in self.df.columns:
            self.df['cmc'].loc[17411] = 1
            self.df['cmc'] = self.df['cmc'].astype('int64')

        if 'oracle_id' in self.df.columns:
            self.df.set_index('oracle_id', inplace=True)

        if 'colors' in self.df.columns:
            self.df['colors'] = self.df['colors'].str[0]
            self.df['colors'].fillna('C', inplace=True)

        if 'color_identity' in self.df.columns:
            self.df['color_identity'] = self.df['color_identity'].str[0]
            self.df['color_identity'].fillna('C', inplace=True)

        if 'keywords' in self.df.columns:
            self.df['keywords'] = self.df['keywords'].str[0]
            self.df['keywords'].fillna('None', inplace=True)

        if 'mana_cost' in self.df.columns:
            self.df['mana_cost'].fillna(
                self.df['cmc'].astype(str), inplace=True)

            l = []
            for val in self.df.mana_cost:
                val = re.sub(r'[{]', '', str(val))
                val = re.sub(r'[}]', '/', val)
                val = val.strip('/')
                l.append(val)
            self.df['mana_cost'] = l
            self.df['mana_cost'] = np.where(
                self.df['mana_cost'] == '',
                self.df['cmc'],
                self.df['mana_cost'])

        # d = ['Card // Card', 'Scheme', 'Vanguard', 'Token', 'Emblem', 'Card', 'Plane']
        # for v in d:
        #     i = self.df[self.df['type_line'].str.startswith(v)].index
        #     self.df.drop(labels = i, inplace=True)

        return self.df

    def modeling_prep_mtg_oracle(self, df):
        """
        Input: Scryfall dataframe
        Output: Cleaned X and y for modeling
        """
        # Drop columns for modeling purposes
        drop_cols = [
            'id',
            'multiverse_ids',
            'tcgplayer_id',
            'cardmarket_id',
            'lang',
            'object',
            'released_at',
            'uri',
            'scryfall_uri',
            'layout',
            'highres_image',
            'image_status',
            'image_uris',
            'games',
            'frame',
            'full_art',
            'textless',
            'booster',
            'story_spotlight',
            'prices',
            'legalities',
            'reserved',
            'foil',
            'nonfoil',
            'card_back_id',
            'artist',
            'artist_ids',
            'illustration_id',
            'border_color',
            'oversized',
            'finishes',
            'scryfall_set_uri',
            'rulings_uri',
            'promo',
            'set',
            'set_uri',
            'set_search_uri',
            'reprint',
            'variation',
            'set_id',
            'prints_search_uri',
            'collector_number',
            'digital',
            'mtgo_id']

        # Drop Null values in text_description column.
        if 'oracle_text' in self.df.columns:
            self.df['oracle_text'].dropna(inplace=True)

        # Creates target vector and drops from feature matrix. Target is
        # related cards.
        if 'related_uris' in self.df.columns:
            target_cards = self.df['related_uris']
            drop_cols.append('related_uris')

        # Drop a million mana_cost card from UnHinged(joke set)
        self.df.drop(index=df[df['name'] == 'Gleemax'].index, inplace=True)

        # Identify columns with over 35% null values and drops them.
        drop_cols_high_nan = [col for col in self.df.columns if (
            self.df[col].isna().sum() / len(self.df) * 100) > 35]
        self.df.drop(columns=drop_cols_high_nan, inplace=True)
        self.df.drop(columns=drop_cols, inplace=True)

        return self.df, target_cards

    def lemma(self, df: pd.DataFrame):
        self.df = df
        self.df.dropna(subset=['oracle_text'], axis=0, inplace=True)
        self.df.drop(self.df.index[self.df['oracle_text'] == ''], inplace=True)
        self.df['oracle_text'] = [re.sub('[^0-9a-zA-Z]+', ' ', i) for i in df.oracle_text]
        nlp = spacy.load('en_core_web_md')
        lemmas = []
        for doc in self.df['oracle_text']:
            lemmas.append([token.lemma_.lower().strip() for token in nlp(str(doc)) if (
                (token.is_stop == False) and (token.is_punct == False) and (token.is_space == False))])
        self.df['lemmas'] = lemmas
        return self.df['lemmas']


if __name__ == '__main__':
    dh = Data_Handling()
    print("Data Handling has been instantiated")
    df = dh.cleaning_scryfall_data()
    print("Successfully created DataFrame Object")
    df['lemmas'] = dh.lemma(df)
    print("Successfully created lemmas from Card Descriptions")
    df.to_csv(filepath)
    print("Data has been updated. Thank you!")
