# Author: Patipol Chiammunchit
# Date: 22 July 2016
# Licence: under the EUPL V.1.1
# Inspiration: https://www-complexnetworks.lip6.fr/~magnien/DynGraph/Software/Delta_Density/

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

from Profiling_Community_Dynamics.computation_module import *
import seaborn as sns
import pandas as pd


def lsplot(linkstream, start_time=None, end_time=None, community=None):
    """
    Plot the linkstream.

    :param linkstream: A Linkstream object.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :rtype: axes
    """

    if community is None: # If community is not assigned, it is assigned to be all users in linkstream
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
        start_time = min(linkstream.linkstream.loc[:, linkstream.column_timestamp])
    if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    community_linkstream = linkstream.linkstream.loc[
        (linkstream.linkstream.loc[:, linkstream.column_sender].isin(community)) & (
            linkstream.linkstream.loc[:, linkstream.column_receiver].isin(community)),] # select links which are occured by users in community.
    community_linkstream = community_linkstream.loc[
        (community_linkstream.loc[:, linkstream.column_timestamp] >= start_time) & (
            community_linkstream.loc[:, linkstream.column_timestamp] <= end_time),] # select links which are in the duration of start_time and end_time.
    community_linkstream = community_linkstream.set_index(np.arange(0, len(community_linkstream))) # set new index for iterating.

    ax = plt.axes() # create axes
    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ] # code for drawing curve
    for i in range(0, len(community_linkstream)):
        verts = [
            (community_linkstream.loc[i, linkstream.column_timestamp],
             community_linkstream.loc[i, linkstream.column_sender]),
            (community_linkstream.loc[i, linkstream.column_timestamp] - 0.5,
             community_linkstream.loc[i, linkstream.column_sender]),
            (community_linkstream.loc[i, linkstream.column_timestamp] - 0.5,
             community_linkstream.loc[i, linkstream.column_receiver]),
            (community_linkstream.loc[i, linkstream.column_timestamp],
             community_linkstream.loc[i, linkstream.column_receiver]),
        ] # create curve point
        path = Path(verts, codes, closed=True) # create curve
        ax.add_patch(patches.PathPatch(path, facecolor='none', lw=2)) # add curve in the axes
        ax.add_artist(
            plt.Circle((community_linkstream.loc[i, linkstream.column_timestamp],
                        community_linkstream.loc[i, linkstream.column_sender]), radius=0.05,
                       color='black')) # draw circle at the sender point
        ax.add_artist(
            plt.Circle((community_linkstream.loc[i, linkstream.column_timestamp],
                        community_linkstream.loc[i, linkstream.column_receiver]), radius=0.05,
                       color='black')) # draw circle at the receiver point

    # config the figure

    ymax = max([max(community_linkstream.loc[:, linkstream.column_sender]),
                max(community_linkstream.loc[:, linkstream.column_receiver])]) + 1
    ymin = min([min(community_linkstream.loc[:, linkstream.column_sender]),
                min(community_linkstream.loc[:, linkstream.column_receiver])]) - 1
    ax.set_xlim([start_time - 2, end_time + 2])
    ax.set_ylim([ymin, ymax])
    ax.set_ylabel('node id')
    ax.set_xlabel('timestamp')
    return ax


def density_2nd_derivative_lsplot(linkstream, start_delta=None, end_delta=None, step=1, start_time=None,
                                  end_time=None,
                                  community=None):
    """
    Plot the evolution of deltadensity according to delta, second derivative of deltadensity, and linkstream in one figure.

    :param linkstream: Linkstream object.
    :param float start_delta: Start delta you would like to compute.
    :param float end_delta: Start delta you would like to compute.
    :param floatstep: step of rising of delta.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :type: list of axes
    """

    if start_delta is None: # If start_delta is not assigned, start_delta will be 0.
        start_delta = 0
    if end_delta is None: # If end_delta is not assigned, end_delta will be last timestamp of linkstream.
        end_delta = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])
    if community is None: # If community is not assigned, it is assigned to be all users in linkstream.
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None: # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])
    fig = plt.figure(figsize=(9, 9)) # create the figure
    axes = [fig.add_subplot(3, 1, 1), fig.add_subplot(3, 1, 2), fig.add_subplot(3, 1, 3)] # add three axes in the figure

    # tspan = max(linkstream.linkstream.loc[:, linkstream.column_timestamp]) + 1

    community_linkstream = linkstream.linkstream.loc[
        (linkstream.linkstream.loc[:, linkstream.column_sender].isin(community)) & (
            linkstream.linkstream.loc[:, linkstream.column_receiver].isin(community)),] # select links which are occured by users in community.
    community_linkstream = community_linkstream.loc[
        (community_linkstream.loc[:, linkstream.column_timestamp] >= start_time) & (
            community_linkstream.loc[:, linkstream.column_timestamp] <= end_time),] # select links which are in the duration of start_time and end_time.
    community_linkstream.loc[:, linkstream.column_timestamp] -= start_time
    community_linkstream = community_linkstream.set_index(np.arange(0, len(community_linkstream)))

    list_delta = list(np.arange(start_delta, end_delta, step)) # create list of delta values which uses to compute delta-density.
    list_deltadensity = delta_density_list(linkstream, delta_list=list_delta, start_time=start_time, end_time=end_time,
                                           community=community) # compute list of delta-density.
    deltadensity_df = pd.DataFrame({'delta': list_delta, 'density': list_deltadensity}) # create pandas dataframe for plotting figure.
    second_derivative = list(np.diff(list_deltadensity, n=2)) # compute second derivative of the evolution of delta-density accoring to delta.
    second_derivative = [0] + second_derivative + [0] # append 0 at the first and last element for shifting the point.

    second_derivative_df = pd.DataFrame({'delta': list_delta, 'second_derivative': second_derivative}) # create pandas dataframe for plotting figure.

    sns.pointplot(x='delta', y='density', data=deltadensity_df, ax=axes[0], fit_reg=False, color='black', join=False) # plot the evolution of delta-density according to delta.
    sns.pointplot(x='delta', y='second_derivative', data=second_derivative_df, ax=axes[1], color='red') # plot the second derivative of the evolution of delta-density accoring to delta.

    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ] # code for drawing curve

    for i in range(0, len(community_linkstream)):
        verts = [
            (community_linkstream.loc[i, linkstream.column_timestamp],
             community_linkstream.loc[i, linkstream.column_sender]),
            (community_linkstream.loc[i, linkstream.column_timestamp] - 0.5,
             community_linkstream.loc[i, linkstream.column_sender]),
            (community_linkstream.loc[i, linkstream.column_timestamp] - 0.5,
             community_linkstream.loc[i, linkstream.column_receiver]),
            (community_linkstream.loc[i, linkstream.column_timestamp],
             community_linkstream.loc[i, linkstream.column_receiver]),
        ] # create curve point
        path = Path(verts, codes, closed=True)  # create curve
        axes[2].add_patch(patches.PathPatch(path, facecolor='none', lw=2)) # add curve in the axes
        axes[2].add_artist(
            plt.Circle((community_linkstream.loc[i, linkstream.column_timestamp],
                        community_linkstream.loc[i, linkstream.column_sender]), radius=0.05,
                       color='black')) # draw circle at the sender point
        axes[2].add_artist(
            plt.Circle((community_linkstream.loc[i, linkstream.column_timestamp],
                        community_linkstream.loc[i, linkstream.column_receiver]), radius=0.05,
                       color='black')) # draw circle at the receiver point

    # Config the figure

    [ax.autoscale_view() for ax in axes]

    axes[2].set_xlim([min(linkstream.linkstream.loc[:, linkstream.column_timestamp]),
                      max(linkstream.linkstream.loc[:, linkstream.column_timestamp])])
    axes[2].set_ylim([min(community) - 1, max(community) + 1])

    axes[1].set_ylabel('second_derivative')
    axes[0].set_ylabel('delta-density')
    axes[2].set_ylabel('node id')
    axes[2].set_xlabel('timestamp')

    return axes


def density_plot(linkstream, start_delta=None, end_delta=None, step=1, start_time=None, end_time=None, community=None):
    """
    Plot the evolution of deltadensity according to delta.

    :param linkstream: Linkstream object.
    :param float start_delta: Start delta you would like to compute.
    :param float end_delta: Start delta you would like to compute.
    :param floatstep: step of rising of delta.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :param community: list of node id.
    :rtype: axes
    """
    if start_delta is None: # If start_delta is not assigned, start_delta will be 0.
        start_delta = 0
    if end_delta is None: # If end_delta is not assigned, end_delta will be 0.
        end_delta = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])
    if community is None: # If community is not assigned, it is assigned to be all users in linkstream.
        community = list(
            np.unique(linkstream.linkstream[[linkstream.column_sender, linkstream.column_receiver]].values))
    if start_time is None: # If start_time is not assigned, it is assigned to be 0.
        start_time = 0
    if end_time is None: # If end_time is not assigned, it is assigned to be 0.
        end_time = max(linkstream.linkstream.loc[:, linkstream.column_timestamp])

    deltadensity_list = []
    delta_list = []

    for delta in range(start_delta, end_delta, step): # Iterate delta in range of delta
        deltadensity_list.append(stream_deltadensity(linkstream, delta, start_time, end_time, community)) # Append stream delta-density in deltadensity_list
        delta_list.append(delta) # Append delta in delta list.

    ax = sns.pointplot(x='x', y='y', data={'x': delta_list, 'y': deltadensity_list}) # plot the figure of evolution of delta-density.

    # Config the figure
    ax.set_xlabel('delta')
    ax.set_ylabel('delta-density')
    ax.set_title('Community: ' + str(community))
    return ax


def max_deltadensity_min_delta_plot(linkstream, communities, start_time=None, end_time=None):
    """


    :param linkstream: Linkstream object.
    :param communities: List of community.
    :param int start_time: Start timestamp.
    :param int end_time: Last timestamp.
    :rtype: axes
    """
    min_delta = []
    max_deltadensity = []
    for community in communities: # Iterate community in communities list
        kpi = max_deltadensity_min_delta(linkstream, start_time, end_time, community) # compute KPI of each communuties
        min_delta.append(kpi['min_delta']) # Append min_delta in list
        max_deltadensity.append(kpi['max_deltadensity']) # Append max_deltadensity in list

    str_communities = [str(x) for x in communities] # casting community to string for pandas dataframe

    data = pd.DataFrame({'min_delta': min_delta, 'max_deltadensity': max_deltadensity, 'community': str_communities}) # create pandas dataframe for plotting the figure
    print(data)
    sns.jointplot(x='min_delta', y='max_deltadensity', data=data) # plot the figure
