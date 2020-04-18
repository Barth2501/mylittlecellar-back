from utils.collection_processing import *
from utils.inverted_index import *


# # Boolean recipes model
# collection = get_pre_processed_collection('./input/recipes.csv')
# inverted_index = build_inverted_index(collection, 1)
# save_inverted_index_pickle(inverted_index, './indexes/index.txt')

# # Vectorial recipes model
# recipes_df = load_data('./input/recipes.csv')
# collection = get_pre_processed_collection('./input/recipes.csv')
# inverted_index = build_inverted_index_vextorial(collection, recipes_df)
# save_inverted_index_pickle(inverted_index, './indexes/index_numbered.txt')

# Area vectorial model
areas_df = load_areas_data('./input/areas.csv')
collection = build_collection_from_df(areas_df)
STOP_WORDS = ['DU','DE','LA','EN','D','ET','L','LE']
collection = remove_stop_words(collection,STOP_WORDS)
inverted_index = build_inverted_index(collection,4)
save_inverted_index_pickle(inverted_index, './indexes/areas_index.txt')
