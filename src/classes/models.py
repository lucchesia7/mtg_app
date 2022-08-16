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
        self.nnm = pickle.load(open(r'{}\model'.format(folder_dir), 'rb'))

    def nn(self, card_name:str):
        self.vect = TfidfVectorizer(preprocessor = dummy_fun,
                                    tokenizer = dummy_fun,
                                    token_pattern=None,
                                    vocabulary=pickle.load(open(r'{}\vectorizer_vocab'.format(folder_dir), 'rb')))
        self.vect.fit([lemmas for lemmas in self.df['lemmas']])
        self.names = []
        self.doc = self.vect.transform([lemmas for lemmas in self.df['lemmas'][self.df['name'] == card_name]])
        self.n_index = self.nnm.kneighbors(self.doc, n_neighbors=11, return_distance=False)

        for index in self.n_index:
            self.names.append(self.df['name'][index].values)
        return self.names
    
if __name__ == '__main__':
    cl = Model()
    names = cl.nn('Drift of the Dead')
    for name in names[0][1:]:
        print(name)