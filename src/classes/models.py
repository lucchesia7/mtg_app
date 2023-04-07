from pathlib import Path
import pandas as pd
import pickle
import os
import re


folder_dir = os.path.join(Path(__file__).parents[1], 'data')
print(folder_dir)


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
        self.string = re.sub(
            r"[A-Za-z]+('[A-Za-z]+)?",
            lambda mo: mo.group(0)[0].upper() +
            mo.group(0)[
                1:].lower() if mo.group(0) not in self.stop_words or self.cap_stop_words and card_name.startswith(
                mo.group(0)) else mo.group(0).lower(),
            card_name)
        self.split = self.string.split()
        print(self.split)
        s = 0
        for name in self.split:
            if '-' in name:
                name = name.title()
                s += 1
            elif name[1] == "'":
                name = name[0:3].upper() + name[3:]
                self.split[s] = name
                s += 1
            else:
                s += 1
        self.val = " ".join(self.split)
        return self.val

    def nn(self, card_name: str):
        """
        Input:
        Card_name: string object, recieved from user input

        Output:
        9 recommended cards
        """
        self.card_name = self.card_name_fix(card_name)
        self.vect = pickle.load(open(f'{folder_dir}/vect', 'rb'))
        self.names = []
        self.doc = self.vect.transform(
            self.df['lemmas'][self.df['name'] == self.card_name])
        self.n_index = self.nnm.kneighbors(
            self.doc, return_distance=False)
        for index in self.n_index[0]:
            if index != self.df[self.df['name'] ==
                                self.card_name].index:
                self.names.append(self.df['name'][index])
        return self.names


if __name__ == '__main__':
    print(Model().card_name_fix('the world tree'))
