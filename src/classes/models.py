from numpy import vectorize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import pickle
import spacy
import os

folder_dir = os.path.dirname(os.path.abspath(__file__))

def dummy_fun(doc):
    return doc

class Model():
    def __init__(self):
        self.df = pd.read_csv(r'C:\Users\Alex Lucchesi\OneDrive\Documents\GitHub\MTG_app\src\classes\oracle_data.csv', 
                              low_memory=False)
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