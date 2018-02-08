# Author: Patipol Chiammunchit
# Date: 22 July 2016
# Licence: under the EUPL V.1.1
# Inspiration: https://www-complexnetworks.lip6.fr/~magnien/DynGraph/Software/Delta_Density/

import numpy as np


def links_deltadensity(linkstream, delta, start_time=None, end_time=None, community=None):
    """
    Compute link delta-density of every possible link in linkstream.

    :param linkstream: Linkstream object.
    :param float delta: Delta you would like to compute delta-density.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :return: map which key are links and value are link delta-density of each links.
    """
    if community is None: # If community is not assigned, it is assigned to be all users in linkstream
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None: # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    links_dict = {}
    linkdeltadensity = {}

    community_linkstream = linkstream.linkstream.loc[
        (linkstream.linkstream.loc[:, linkstream.column_sender].isin(community)) & (
            linkstream.linkstream.loc[:, linkstream.column_receiver].isin(community)),] # select links which are occured by users in community.
    community_linkstream = community_linkstream.loc[
        (community_linkstream.loc[:, linkstream.column_timestamp] >= start_time) & (
            community_linkstream.loc[:, linkstream.column_timestamp] <= end_time),] # select links which are in the duration of start_time and end_time.
    community_linkstream = community_linkstream.set_index(np.arange(0, len(community_linkstream))) # set new index for iterating.

    for i in range(0, len(community_linkstream)): # Iterate every link in linkstream
        link = frozenset([community_linkstream.at[i, linkstream.column_sender],
                          community_linkstream.at[i, linkstream.column_receiver]]) # create link
        if links_dict.get(link) is None: # Append link as key in dictionary if this link appears for the first time.
            links_dict[link] = [start_time, 0, 1] # the value of dictionary is the list which contains three element, timestamp of last link, current value of delta-density, and number of link.

        if links_dict[link][2] == 1: # If this link appears for the first time, the current value of delta-density is equal to tau[0] minus delta (see the formular of link delta-density).
            links_dict[link][1] += max((community_linkstream.at[i, linkstream.column_timestamp] - start_time) - delta,
                                       0)
        else: # If this link does not appear for the first time, the current value of delta-density is plus with tau[i] minus delta (see the formular of link delta-density).
            links_dict[link][1] += max(
                (community_linkstream.at[i, linkstream.column_timestamp] - links_dict[link][0]) - delta, 0)
        links_dict[link][2] += 1 # update number of link.
        links_dict[link][0] = community_linkstream.at[i, linkstream.column_timestamp] # update timestamp of last link.

    for link in links_dict:
        links_dict[link][1] += max(((end_time - start_time) - links_dict[link][0]) - delta, 0) # the current value of delta-density is plus with last tau minus delta (see the formular of link delta-density).
        linkdeltadensity[link] = 1 - float(links_dict[link][1]) / ((end_time - start_time) - delta) # compute link delta-density.
    return linkdeltadensity # return dictionary of link with its own link delta-density.


def stream_deltadensity(linkstream, delta, start_time=None, end_time=None, community=None):
    """
    Compute stream delta-density of community with one delta value.

    :param linkstream: Linkstream object.
    :param float delta: Delta you would like to compute delta-density.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :return: stream delta-density of community.
    :rtype: float
    """
    if community is None:  # If community is not assigned, it is assigned to be all users in linkstream
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None:  # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None:  # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    if linkstream.linkstream.empty:
        return 0

    node_amount = len(community) # get number of users
    link_deltadensity = links_deltadensity(linkstream, delta, start_time, end_time, community) # compute link delta-density of every link in community.
    sum_links_deltadensity = 0
    for link, density in link_deltadensity.items():
        sum_links_deltadensity += density # sum the link delta-density of every link in community
    return (2 * sum_links_deltadensity / ((node_amount) * (node_amount - 1))) # compute stream delta-density of the community and return it.


def delta_density_list(linkstream, delta_list, start_time=None, end_time=None, community=None):
    """
    Compute stream delta-density of community with many delta values.

    :param linkstream: Linkstream object.
    :param float delta: Delta you would like to compute delta-density.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :return: list of stream delta-density.
    """
    if community is None:  # If community is not assigned, it is assigned to be all users in linkstream
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None:  # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None:  # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    density_list = []
    for delta in delta_list: # Iterate every delta in delta_list
        density_list.append(stream_deltadensity(linkstream, delta, start_time, end_time, community)) # Append delta-density of each delta values in density_list

    return density_list # return list of stream delta-density.


def max_deltadensity_min_delta(linkstream, start_time=None, end_time=None, community=None):
    """
    Find the smallest delta where stream delta-density is maximum and max delta-density.

    :param linkstream: Linkstream object.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :return: map which contains smallest delta where stream delta-density is maximum and max delta-density.
    """
    if community is None:  # If community is not assigned, it is assigned to be all users in linkstream
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None:  # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None:  # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    community_linkstream = linkstream.linkstream.loc[
        (linkstream.linkstream.loc[:, linkstream.column_sender].isin(community)) & (
            linkstream.linkstream.loc[:, linkstream.column_receiver].isin(community)),] # select links which are occured by users in community.
    community_linkstream = community_linkstream.loc[
        (community_linkstream.loc[:, linkstream.column_timestamp] >= start_time) & (
            community_linkstream.loc[:, linkstream.column_timestamp] <= end_time),] # select links which are in the duration of start_time and end_time.
    community_linkstream = community_linkstream.set_index(np.arange(0, len(community_linkstream))) # set new index for iterating.

    last_timestamp = {}
    max_timestamp = {}

    for i in range(0, len(community_linkstream)): # Iterate every link in community link stream
        if not community_linkstream.empty:
            link = frozenset([community_linkstream.at[i, linkstream.column_sender],
                              community_linkstream.at[i, linkstream.column_receiver]]) # create link
            max_timestamp[link] = max(max_timestamp.get(link, 0),
                                      community_linkstream.at[i, linkstream.column_timestamp] - last_timestamp.get(
                                          link, start_time)) # find the maximum time difference of each links.
            last_timestamp[link] = community_linkstream.at[i, linkstream.column_timestamp]
            if i == len(community_linkstream) - 1: # find the maximum time difference of each links (for last link)
                max_timestamp[link] = max(max_timestamp.get(link, 0), end_time - last_timestamp.get(link, 0))
                last_timestamp[link] = end_time

    min_delta = 0
    for key, val in max_timestamp.items():
        min_delta = max(min_delta, val) # find the maximum time difference of every link (that is min delta where delta-density is maximum).

    max_deltadensity = stream_deltadensity(linkstream, min_delta, start_time, end_time, community) # compute max delta-density of community.

    return {'min_delta': min_delta, 'max_deltadensity': max_deltadensity}
