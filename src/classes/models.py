from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import os
import re


folder_dir = os.path.join(Path(__file__).parents[1], 'data')


def dummy_fun(doc):
    return doc


class Model():
    def __init__(self):
        self.df = pd.read_csv(
            f'{folder_dir}/oracle_data.csv',
            low_memory=False)
        self.nnm = pickle.load(open(f'{folder_dir}/model', 'rb'))
        self.stop_words = ['on', 'the', 'of', 'and']
        self.cap_stop_words = [w.title() for w in self.stop_words]

    def card_name_fix(self, card_name: str):
        self.string = re.findall('[A-Za-z\']+(?:\`[A-Za-z]+)?',card_name)
        # print(self.string)
        # for name in self.string:
        #     print(name)
        #     if '-' in name:
        #         name = name.title()
        #     elif name[0].islower() and name not in self.stop_words or card_name.startswith(name):
        #         name = name.title()
        #         print(name)
        #     elif name[0].isupper() and name in self.cap_stop_words and not card_name.startswith(name):
        #         name = name.lower()
        #         print(name)
        self.string = ' '.join(self.string)
        # print(self.string)
        return self.string

    def nn(self, card_name: str):
        """
        Input: 
        Card_name: string object, recieved from user input

        Output:
        9 recommended cards
        """
        self.vect = TfidfVectorizer(
            preprocessor=dummy_fun,
            tokenizer=dummy_fun,
            token_pattern=None,
            vocabulary=pickle.load(
                open(
                    f'{folder_dir}/vectorizer_vocab',
                    'rb')))
        self.vect.fit(self.df['lemmas'])
        self.names = []
        self.doc = self.vect.transform(
            self.df['lemmas'][self.df['name'] == self.card_name_fix(card_name)])
        self.n_index = self.nnm.kneighbors(
            self.doc, return_distance=False)
        for index in self.n_index[0]:
            if index != self.df[self.df['name'] ==
                                self.card_name_fix(card_name)].index:
                self.names.append(self.df['name'][index])
        return self.names

if __name__ == '__main__':
    # print(Model().card_name_fix("Kozilek's ChanNelEr"))
    print(Model().nn('The World Tree'))

