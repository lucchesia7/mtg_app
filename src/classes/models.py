from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import os

# folder_dir = os.path.dirname(os.path.abspath(__file__))
folder_dir = os.path.join(Path(__file__).parents[1], 'data')

def dummy_fun(doc):
    return doc

class Model():
    def __init__(self):
        self.df = pd.read_csv(f'{folder_dir}/oracle_data.csv', low_memory=False)
        # self.nnm = pickle.load(open(r'{}\model_1'.format(folder_dir), 'rb'))
        self.nnm = pickle.load(open(f'{folder_dir}/model_1', 'rb'))
        self.stop_words = ['on', 'the', 'of']
        self.cap_stop_words = [w.title() for w in self.stop_words]
    
    def card_name_fix(self, card_name:str):
        self.split = card_name.split()
        self.string = ''
        # print(self.split)
        for name in self.split:
            if '-' in name:
                name = name.title()
            elif name[0].islower() and name not in self.stop_words or card_name.startswith(name):
                # print(f'{name} is lower-cased and not in stop words')
                name = name.title()
            elif name[0].isupper() and name in self.cap_stop_words and card_name.startswith(name) !=1:
                # print(f'{name} is upper-cased and is in stop words')
                name = name.lower()
            self.string += (' ' + name)
            self.string = self.string.strip()
        # print(self.string)
            

        return self.string

    def nn(self, card_name:str):
        self.vect = TfidfVectorizer(preprocessor = dummy_fun,
                                    tokenizer = dummy_fun,
                                    token_pattern=None,
                                    # vocabulary=pickle.load(open(r'{}\vectorizer_vocab_1'.format(folder_dir), 'rb')
                                    vocabulary=pickle.load(open(f'{folder_dir}/vectorizer_vocab_2', 'rb')))
        self.vect.fit(self.df['lemmas'])
        self.names = []
        self.doc = self.vect.transform(self.df['lemmas'][self.df['name'] == self.card_name_fix(card_name)])
        self.n_index = self.nnm.kneighbors(self.doc, n_neighbors=13, return_distance=False)

        for index in self.n_index[0]:
            if index != self.df[self.df['name'] == self.card_name_fix(card_name)].index:
                self.names.append(self.df['name'][index])
        return self.names
if __name__ == '__main__':
    model = Model()
    # print(model.card_name_fix('elisha, The infinite'))
    # print(model.card_name_fix('the world tree'))
    # print(model.card_name_fix('The ur-Dragon'))
    print(model.nn('the world tree'))
    # print(filepath)