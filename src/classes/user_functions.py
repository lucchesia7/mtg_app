from pathlib import Path
from PIL import Image
from io import BytesIO
import requests
from .models import Model
import pandas as pd
import ast
import os


filepath = os.path.join(Path(__file__).parents[1], 'data/oracle_data.csv')


class User_Functions():
    def __init__(self):
        self.df = pd.read_csv(filepath, low_memory=False)
        self.token_df = self.df[self.df['type_line'].str.contains(
            'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]
        # self.df = self.df[~self.df['type_line'].str.contains(
        #     'Card // Card|Token|Scheme|Vanguard|Emblem|Card|Plane', regex=True)]

    def img_return(self, card_name: str):
        """
        Input: Card name as a string. String set to autopopulate with Sol Ring.
        Bug: Dual sided cards are not returning. Desired return would be both sides of the card, if not just the side requested.
        Would like to show 10 cards that have the same first few letters for users to choose from in a dropdown menu
        Output: Fully-detailed card image returned as output.
        """
        s = self.df[self.df['name'] ==
                    Model().card_name_fix(card_name)]['image_uris']
        for k in s:
            img_dic = ast.literal_eval(k)
        img_str = img_dic['normal']
        response = requests.get(img_str)
        img = Image.open(BytesIO(response.content))
        return img

    def token_generation(
            self,
            token_name: str,
            token_type: str,
            token_count: int = 1):
        """
        Input:
        token_name : the name of the token you wish to create. Must be str data type\n
        token_type: The type of token you wish to create. This can be Emblems, Planes, Tokens, and Vanguards.\n
        token_count: The number of tokens you wish to create
        """

        if token_type.lower() == 'tokens':
            self.ss = self.token_df[self.token_df['type_line'].str.contains(
                'Token')]
            self.s = self.ss[self.ss['name'].str.lower().str.contains(
                token_name.lower())]['image_uris']

        elif token_type.lower() == 'emblems':
            self.ss = self.token_df[self.token_df['type_line'].str.contains(
                'Emblems')]
            self.s = self.ss[self.ss['name'].str.lower().str.contains(
                token_name.lower())]['image_uris']

        else:
            self.s = self.token_df[self.token_df['name'].str.lower(
            ).str.contains(token_name.lower())]['image_uris']

        for k in self.s:
            img_dic = ast.literal_eval(k)
        img_str = img_dic['normal']
        response = requests.get(img_str)
        img = Image.open(BytesIO(response.content))

        return img

    def recommended_cards(self, card_name: str):
        """
        Input: Card name as str.
        Output: 10 related cards to user input card name.
        """

        model = Model()
        names = model.nn(model.card_name_fix(card_name))
        return [self.img_return(name) for name in names]

    def token_generator(self, token_type: str, token_count: int):
        pass
