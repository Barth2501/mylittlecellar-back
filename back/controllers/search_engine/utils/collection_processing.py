import pandas as pd
import re
import collections
from nltk.tokenize import RegexpTokenizer
import unidecode


def load_data(filename):
    recipes_df = pd.read_csv(filename, header=None, usecols=[
                             0, 1, 2, 5], names=['id', 'name', 'ingredients', 'category_id'])

    def replace(x):
        res = x.copy()
        if x.isna()['ingredients']:
            res['ingredients'] = x['name']
        return res

    recipes_df = recipes_df.apply(replace, axis=1)
    return recipes_df

def load_areas_data(filename):
    areas_df = pd.read_csv(filename, header=None, usecols=[0,1], names=['id','ingredients'])
    return areas_df

def build_corpus(recipes_df):
    corpus = {}
    for recipe in enumerate(recipes_df.itertuples()):
        corpus[recipe[1].id] = []
        ingredients = recipe[1].ingredients.split(',')
        for ingredient in ingredients:
            numbers_list = re.findall(r'[0-9]+', ingredient)
            numbers_list += ['-', '/', ',', '(', ')', "'"]
            for nbr in numbers_list:
                ingredient = ingredient.replace(nbr, ' ')
            ingredient = ingredient.strip()
            corpus[recipe[1].id] += ingredient.split(' ')
    return corpus


def recipe_tokenize(recipe):
    if type(recipe) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokenizer = RegexpTokenizer(r'(\w+)')
        tokens = tokenizer.tokenize(recipe)
        filt_tokens = []
        for token in tokens:
            if not re.match(r'.*\d+.*', token):
                filt_tokens.append(token.upper())
        return filt_tokens

def remove_accent(text):
    return unidecode.unidecode(text)


def build_collection_from_df(recipes_df):
    corpus = {}
    for recipe in enumerate(recipes_df.itertuples()):
        text = remove_accent(recipe[1].ingredients)
        corpus[recipe[1].id] = recipe_tokenize(text)
    return corpus


def count_frequency(collection):
    tokens_count = collections.Counter()
    for key in collection.keys():
        count = collections.Counter(collection[key])
        tokens_count.update(count)
    return tokens_count


def n_most_common_tokens(collection, n):
    tokens_count = count_frequency(collection)
    n_most_common_tokens = tokens_count.most_common(n)
    return n_most_common_tokens


STOP_WORDS = ['DE', 'G', 'AUX', 'À', 'CUIL',
              'SOUPE', 'D', 'CL', 'OU', 'DU',
              'MON', 'AU', 'DES', 'LE', 'LES',
              'LA', 'EN', 'KG', 'POUR', 'ET', 'LIVRE', 'L', 'RECETTE']

# Fonction permettant de filtrer la collection des mots vides


def remove_stop_words(collection, stop_word_file):
    collection_filtered = {}
    for i in collection:
        collection_filtered[i] = []
        for j in collection[i]:
            if j not in stop_word_file:
                collection_filtered[i].append(j)
    return collection_filtered


def pre_process_collection(collection):
    collection = remove_stop_words(collection, STOP_WORDS)
    return collection


def get_pre_processed_collection(filename):
    recipes_df = load_data(filename)
    collection = build_collection_from_df(recipes_df)
    return pre_process_collection(collection)

def get_term_weigth(document_id, term, recipes_df):
    step_list = recipes_df[recipes_df.id==document_id]['ingredients'].reset_index()['ingredients'][0]
    step_list = step_list.split(',')
    for pos,ingredients in enumerate(step_list):
        if re.findall(term,ingredients.upper()):
            return weigth_function(pos)
    return 0

def weigth_function(pos,ratio=1.2,first_val=1):
    return (1/ratio)**(pos)*first_val
