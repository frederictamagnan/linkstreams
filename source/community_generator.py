import pandas as pd
import numpy as np
import itertools

def community_generator(linkstreams) :
    """
    Generate all community that possible in the link streams.
    :param linkstreams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :return: list of communities.
    """
    node_list = np.unique(linkstreams[['u', 'v']].values)
    communities = []
    for i in range(2,len(node_list)+1) :
        communities += list(itertools.combinations(node_list,i))
    return list(map(list,communities))