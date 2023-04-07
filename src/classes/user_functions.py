from pathlib import Path
from PIL import Image
from io import BytesIO
import requests
from models import Model
import pandas as pd
import ast
import os


folder_dir = os.path.join(Path(__file__).parents[1], 'data')


class User_Functions():
    def __init__(self):
        self.df = pd.read_csv(
            f'{folder_dir}/oracle_data.csv',
            low_memory=False)
        self.token_df = pd.read_csv(f'{folder_dir}/token_data.csv')

    def img_return(self, card_name: str):
        """
        Input: Card name as a string.
        Bug: Dual sided cards are not returning. Desired return would be both sides of the card, if not just the side requested.
        Would like to show 10 cards that have the same first few letters for users to choose from in a dropdown menu

        This function will take a card string and return an image output to the user of the specified card. Card name can be lowercased, uppercased, type-cased. But must be spelled properly.

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

    def recommended_cards(self, card_name: str):
        """
        Input: Card name as str.
        Output: 10 related cards to user input card name.
        """

        model = Model()
        names = model.nn(card_name)
        return [self.img_return(name) for name in names]

    def token_generator(self, token_type: str, token_count: int):
        # TODO
        pass


if __name__ == '__main__':
    User_Functions().recommended_cards('Sol Ring')