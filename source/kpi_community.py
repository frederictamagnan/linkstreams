from delta_density import *
import numpy as np
from pandas.io.parsers import read_csv

def max_stream_deltadensity(link_streams,community) :
    """
    Compute the max delta-density and smallest delta where delta-density is max.
    :param link_streams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :param community: list of node in community eg. [1,2,5].
    :return: list that contain 2 value, first value is smallest delta where delta-density is max and second value is max delta-density
    """
    df_community = link_streams[(link_streams.u.isin(community)) & (link_streams.v.isin(community))]
    df_community = df_community.set_index(np.arange(0, len(df_community)))
    tspan = max(link_streams.t) + 1
    max_deltadensity = stream_deltadensity(df_community,tspan-1,tspan)

    last_timestamp = {}
    max_timestamp = {}

    for i in range(0, len(df_community)):
        if not df_community.empty :
            link = frozenset([df_community.at[i, 'u'], df_community.at[i, 'v']])
            max_timestamp[link] = max(max_timestamp.get(link, 0), df_community.at[i, 't'] - last_timestamp.get(link, 0))
            last_timestamp[link] = df_community.at[i, 't']
            if i == len(df_community)-1 :
                max_timestamp[link] = max(max_timestamp.get(link, 0), tspan - last_timestamp.get(link, 0))
                last_timestamp[link] = tspan
    max_delta = 0
    for key, val in max_timestamp.items():
        max_delta = max(max_delta,val)
    return [max_delta,max_deltadensity]

def community_deltadensity_sequence(link_streams,community,range=-1,start_delta=-1,stop_delta=-1,step=1.0) :
    """
    Compute the list of delta-density according to the list of delta.
    :param link_streams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :param community: list of node in community eg. [1,2,5].
    :param range: the maximum timestamp you would like to consider. If range is -1, range is equal to the maximum timestamp in link_streams plus 1.
    :param start_delta: the first delta you would like to compute.
    :param stop_delta: the last delta you would like to compute.
    :param step: the step of delta that is increasing.
    :return: list that contain two list, the first list is the list of delta and the second list is the list of delta-density.
    """
    df_community = link_streams[(link_streams.u.isin(community)) & (link_streams.v.isin(community))]
    df_community = df_community.set_index(np.arange(0,len(df_community)))
    list_stream_delta_density = []
    tspan = max(link_streams.t) + 1
    start = 0
    stop = tspan - 1
    if range != -1 : tspan = range
    if start_delta != -1 : start = start_delta
    if stop_delta != -1 : stop = stop_delta
    for delta in np.arange(start,stop,step) :
        list_stream_delta_density.append(stream_deltadensity(df_community,delta,tspan))
    return {'delta':list(np.arange(start,stop,step)),'density':list_stream_delta_density}


def characteristic_delta(link_streams,community) :
    """
    Find the delta that make the highest derivative of delta-density.
    :param link_streams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :param community: list of node in community eg. [1,2,5].
    :return: characteristic delta.
    """
    seq_deltadensity = community_deltadensity_sequence(link_streams=link_streams, community=community, step=0.1)
    diff_deltadensity = list(np.diff(seq_deltadensity[1]))
    diff_time = list(np.diff(seq_deltadensity[0]))
    diff = list(map(lambda x,y : x/y,diff_deltadensity,diff_time))
    max_diff = diff.index(max(diff)) + 1
    cur_density = seq_deltadensity[1][max_diff]
    return [max_diff/10,cur_density]