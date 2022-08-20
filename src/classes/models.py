from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import pickle
import os

folder_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(Path(__file__).parents[1], 'data/oracle_data.csv')

def dummy_fun(doc):
    return doc

class Model():
    def __init__(self):
        self.df = pd.read_csv(filepath, low_memory=False)
        self.nnm = pickle.load(open('{}/model'.format(folder_dir), 'rb'))
        self.stop_words = ['on', 'the', 'of']
        self.cap_stop_words = [w.capitalize() for w in self.stop_words]
    
    def card_name_fix(self, card_name:str):
        self.split = card_name.split()
        self.string = ''
        for name in self.split:
            if '-' in name:
                name = name.title()
            elif name[0].islower() and name not in self.stop_words:
                name = name.title()
            elif name[0].isupper() and name in self.cap_stop_words:
                name = name.lower()
            else:
                name = name.title()
                print(name + 'else')
            self.string += (' ' + name)
            self.string = self.string.strip()
        print(self.string)
        return self.string

    def nn(self, card_name:str):
        self.vect = TfidfVectorizer(preprocessor = dummy_fun,
                                    tokenizer = dummy_fun,
                                    token_pattern=None,
                                    vocabulary=pickle.load(open('{}/vectorizer_vocab'.format(folder_dir), 'rb')))
        self.vect.fit(self.df['lemmas'])
        self.names = []
        self.doc = self.vect.transform(self.df['lemmas'][self.df['name'] == self.card_name_fix(card_name)])
        self.n_index = self.nnm.kneighbors(self.doc, n_neighbors=13, return_distance=False)

        for index in self.n_index[0][1:]:
            self.names.append(self.df['name'][index])
        return self.names
if __name__ == '__main__':
    model = Model()
    print(model.nn('pIr, iMagiNative raScal'))
