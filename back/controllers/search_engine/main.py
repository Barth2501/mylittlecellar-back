import re
import os
from .utils.collection_processing import *
# from utils.boolean import *
from .utils.inverted_index import *
from .utils.vectorial import *


def find_recipes(query, model):
    
    if model == 'boolean':
        recipes_df = load_data('./search_egine/input/recipes.csv')
        inverted_index = load_inverted_index_pickle('./indexes/index.txt')
        result = processing_boolean_query_with_inverted_index(
            BooleanOperator, FLAGS.query, inverted_index)
        print(recipes_df[recipes_df['id'].isin(result)])

    elif model == 'vectorial':
        recipes_df = load_data('back/controllers/search_engine/input/recipes.csv')
        inverted_index = load_inverted_index_pickle('back/controllers/search_engine/indexes/index_numbered.txt')
        result = vectorial_search(inverted_index,query)
        return result

def find_area(query):
    inverted_index = load_inverted_index_pickle('back/controllers/search_engine/indexes/areas_index.txt')
    query = query_transformation(query, inverted_index)
    print(query)
    result = area_vectorial_search(inverted_index,query)
    print(result)
    return result[0][0]     
