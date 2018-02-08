from pandas.io.parsers import *
from delta_density import *
import pandas as pd
import json

def community_reader(community):
    """
    Transform wrong format json file to be a new one
    :param community: dictionary of community which import from json file
    :return: community dictionary
    """
    community_dict = {}
    community_node_string = community['context'][1:len(community['context']) - 1].split(',')
    community_node = list(map(int, community_node_string))
    community_dict['initiator'] = int(community['initiator'])
    community_dict['node_id'] = [community_dict['initiator']]
    community_dict['node_id'] += community_node
    community_dict['min_time'] = int(community['min_time'])
    community_dict['max_time'] = int(community['max_time'])
    return community_dict


def community_linkstream(link_streams, community):
    df =  link_streams.loc[(link_streams.loc[:,'u'].isin(community) & link_streams.loc[:,'v'].isin(community)), ]
    df = df.set_index(np.arange(0, len(df)))
    return df


def get_linkstream(link_streams_path):
    link_stream = read_csv(link_streams_path)
    link_stream = link_stream.drop(link_stream.columns[0], axis=1)
    link_stream.columns = ['v', 'u', 't']
    link_stream.t -= min(link_stream.t)
    link_stream = link_stream.sort_values(['t'],ascending = ['1'])
    return link_stream

def get_communities(link_stream, communities_path):
    with open(communities_path) as data_file:
        communities = json.load(data_file)
    community_list = []
    for community in communities:
        community = community_reader(community)
        community_list.append(community['node_id'])

    return community_list


def get_input(link_streams_path, communities_path):
    linkstream = get_linkstream(link_streams_path)
    communities = get_communities(linkstream, communities_path)
    return {'linkstream': linkstream, 'community': communities}



# data = get_input("../data/board/linkstream.csv", "../data/board/communities.json")
#
# density_list_list = pd.DataFrame(columns=['1 hour','1 day','3 days','7 days'])
#
# for comlink in data['community_linkstream']:
#     density_list = delta_density_list(link_stream=comlink,delta_list=[3600,86400,259200,604800],tspan=max(data['whole_linkstream'].t)-min(data['whole_linkstream'].t))
#     density_list_list = density_list_list.append({'1 hour': density_list[0],'1 day': density_list[1],'3 days': density_list[2],'7 days': density_list[3]},ignore_index=True)
#
# print(density_list_list)