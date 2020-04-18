import re
from nltk.tokenize import RegexpTokenizer
from collections import OrderedDict
import unidecode


def remove_non_index_term(query, inverted_index):
    query_filt = []
    for token in query:
        if token in inverted_index:
            query_filt.append(token)
    return query_filt

def remove_accent(text):
    return unidecode.unidecode(text)

def tokenize_query(query):
    tokenized_query = []
    tokenizer = RegexpTokenizer(r'(\w+)')
    text = remove_accent(query)
    tokens = tokenizer.tokenize(text)
    for token in tokens:
        if not re.match(r'.*\d+.*', token):
            tokenized_query.append(token.upper())
    return tokenized_query


def query_transformation(query, inverted_index):
    tokenized_query = tokenize_query(query)
    filtered_query = remove_non_index_term(tokenized_query, inverted_index)
    return filtered_query


def vectorial_search(inverted_index, query):
    query = query_transformation(query, inverted_index)
    result = {}
    norm_factor_q = 0
    for term in query:
        weigth_q = 1
        norm_factor_q += 1
        if term in inverted_index.keys():
            for document,weigth_doc,norm_factor in inverted_index[term]:
                if document in result.keys():
                    result[document] += weigth_doc*weigth_q/(norm_factor)**(0.5)
                else:
                    result[document] = weigth_doc*weigth_q/(norm_factor)**(0.5)
    
    ordered_list = [[key,result[key]] for key in result.keys()]
    return sorted(ordered_list, key=lambda x: x[1], reverse=True)
    

def area_vectorial_search(inverted_index, query):
    result = {}
    for term in query:
        weigth_q = 1
        if term in inverted_index.keys():
            for document,length_doc in inverted_index[term]:
                weigth_doc = 1
                if document in result.keys():
                    result[document] += weigth_doc*weigth_q/(length_doc)**(0.5)
                else:
                    result[document] = weigth_doc*weigth_q/(length_doc)**(0.5)
    
    ordered_list = [[key,result[key]] for key in result.keys()]
    return sorted(ordered_list, key=lambda x: x[1], reverse=True)