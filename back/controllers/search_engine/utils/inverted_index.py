from collections import OrderedDict
from .collection_processing import get_term_weigth
import pickle


def build_inverted_index(collection, type_index):
    # On considère ici que la collection est pré-traitée
    inverted_index = OrderedDict()
    if type_index == 1:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document not in inverted_index[term]:
                        inverted_index[term].append(document)
                else:
                    inverted_index[term] = [document]
    elif type_index == 2:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document] = inverted_index[term][document] + 1
                    else:
                        inverted_index[term][document] = 1
                else:
                    inverted_index[term] = OrderedDict()
                    inverted_index[term][document] = 1
    elif type_index == 3:
        for document in collection:
            n = 0
            for term in collection[document]:
                n = n+1
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document][0] = inverted_index[term][document][0] + 1
                        inverted_index[term][document][1].append(n)
                    else:
                        inverted_index[term][document] = [1, [n]]
                else:
                    inverted_index[term] = OrderedDict()
                    inverted_index[term][document] = [1, [n]]           
    elif type_index == 4:
        for document in collection:
            length = len(collection[document])
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document not in inverted_index[term]:
                        inverted_index[term].append([document, length])
                else:
                    inverted_index[term] = [[document, length]]
    return inverted_index

def build_inverted_index_vextorial(collection, recipes_df):
    norm_factor_dict = {}
    inverted_index = OrderedDict()
    for document in collection:
        norm_factor_dict[document] = 0
        for term in collection[document]:
            weigth_term = get_term_weigth(document, term, recipes_df)
            if term in inverted_index.keys():
                if document not in inverted_index[term]:
                    inverted_index[term].append([document,weigth_term])
            else:
                inverted_index[term] = [[document,weigth_term]]
            norm_factor_dict[document] += weigth_term**2
    for term in inverted_index:
        for i,(document,weigth) in enumerate(inverted_index[term]):
            norm_factor = norm_factor_dict[document]
            inverted_index[term][i] = [document,weigth,norm_factor]
    return inverted_index

# Ecriture sur disque


def save_inverted_index_pickle(inverted_index, filename):
    with open(filename, "wb") as f:
        pickle.dump(inverted_index, f)
        f.close()


# Chargement

def load_inverted_index_pickle(filename):
    with open(filename, 'rb') as fb:
        index = pickle.load(fb)
        return index
