from data_extraction import *
import pandas as pd
import numpy as np
import operator

def explore_linkstream(linkstream):
    """
    Doing the data exploration of link stream
    :param linkstream: pandas dataframe that consist of column t (int: the timestamp of link), u (int: the id of node), v (int: the id of node).
    :return: void
    """

    users = list(np.unique(linkstream[['u', 'v']].values))
    timestamp = list(np.unique(linkstream[['t']].values))
    sorted(timestamp)

    timestamp_diff = list(np.diff(timestamp))
    print("============================================================")
    print("Describe size of community: ")
    print("Users: " + str(len(users)))
    print("Link: " + str(len(linkstream)))
    print("timestamp: " + str(len(timestamp)))

    print("============================================================")
    print("Describe timestamp of link (minus min timestamp): ")
    print(pd.Series(timestamp-min(timestamp)).describe())

    print("============================================================")
    print("Describe time range of two close link: ")
    print(pd.Series(timestamp_diff).describe())

    users_sending_message = []
    for user in users:
        user_sending_message = linkstream.loc[(linkstream.u == user), ]
        users_sending_message.append(len(user_sending_message))

    print("============================================================")
    print("Describe message sending of users: ")
    print(pd.Series(users_sending_message).describe())

    link_dict = {}

    for i in range(0,len(linkstream)):
        l = frozenset([int(linkstream.loc[i,'u']),int(linkstream.loc[i,'v'])])
        link_dict[l] = link_dict.get(l,0) + 1

    print("============================================================")
    print("Describe interaction of all pair of users: ")
    print(pd.Series(list(link_dict.values())).describe())


def explore_communities(communities):
    """
    Doing the data exploration of communities
    :param communities: dictionary which contains two keys, community_linkstream and community. The first key, community_linkstream, contains list of pandas dataframe which contain link stream and the second key contains list of community.
    :return: void
    """
    communities_size = []
    user_dict = {}
    for community in communities['community']:
        communities_size.append(len(community))
        for user in community:
            user_dict[user] = user_dict.get(user,0) + 1

    print("============================================================")
    print("Describe the amount of group that user joined: ")
    print(pd.Series(list(user_dict.values())).describe())

    print("============================================================")
    print("Describe size of community: ")
    print(pd.Series(communities_size).describe())



linkstream = get_linkstream('../data/board/linkstream.csv')
explore_linkstream(linkstream)

# communities = get_communities(link_stream=linkstream,communities_path='../data/board/communities.json')
# explore_communities(communities)