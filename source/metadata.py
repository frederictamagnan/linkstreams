from kpi_community import *
from pandas.io.parsers import *
from data_extraction import *
import pandas as pd
import numpy as np

data = get_input('../data/board/linkstream.csv','../data/board/communities.json')
linkstream = data['linkstream']
communities = data['community']

metadata = pd.DataFrame(columns=['community_id', 'community', 'number_of_node', 'number_of_link', 'whole_time_range(second)', 'unique_timestamp','max_deltadensity', 'min_delta_where_max_deltadensity', 'average_message_sending_per_user'])
for community in communities:
    com_link = community_linkstream(linkstream, community)
    number_of_node = len(community)
    number_of_link = len(com_link)
    whole_time_range = max(com_link.t) - min(com_link.t)
    kpi = max_stream_deltadensity(linkstream, community)
    max_deltadensity = kpi[1]
    min_delta = kpi[0]
    unique_timestamp = len(list(np.unique(com_link.t)))

    average_message_sending = 0
    for user in community:
        user_linkstream = com_link.loc[com_link.u == user, ]
        average_message_sending += len(user_linkstream)

    average_message_sending /= len(community)
    row_metadata = pd.DataFrame({'community_id': [communities.index(community)],'community': [str(community)], 'number_of_node': [number_of_node], 'number_of_link': [number_of_link], 'whole_time_range(second)': [whole_time_range], 'unique_timestamp': [unique_timestamp], 'max_deltadensity': [max_deltadensity], 'min_delta_where_max_deltadensity': [min_delta], 'average_message_sending_per_user': [average_message_sending]})

    metadata = metadata.append(row_metadata)

metadata.to_csv('../data/metadata/metadata.csv', index=False)