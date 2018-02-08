from kpi_community import *
from community_clustering import *
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def plot_seq_community_deltadensity(link_streams,community,start_delta=-1,stop_delta=-1,step=1) :
    """
    Plot the figure of delta-density according to delta.
    :param link_streams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :param community: list of node in community eg. [1,2,5].
    :param step: step of delta which is use to plot the figure.
    :return: void
    """
    tspan = max(link_streams.t) + 1
    start = 0
    stop = tspan - 1
    if start_delta != -1: start = start_delta
    if stop_delta != -1: stop = stop_delta
    seq_deltadensity = community_deltadensity_sequence(link_streams=link_streams,community=community,range=tspan,start_delta=start,stop_delta=stop,step=step)
    data = pd.DataFrame({'delta':seq_deltadensity['delta'],'density':seq_deltadensity['density']})
    sns.lmplot(x='delta',y='density',data=data,fit_reg=False,sharex=False,sharey=False)
    # sns.plt.ylim([-0.0001,0.002])
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()


def plot_seq_communities_deltadensity(link_streams,community_list,start_delta=-1,stop_delta=-1,step=1):
    tspan = max(link_streams.t) + 1
    start = 0
    stop = tspan - 1
    if start_delta != -1: start = start_delta
    if stop_delta != -1: stop = stop_delta
    deltadensity_list = []
    delta_list = []
    community_id = []
    d = list(np.arange(start,stop,step))
    count = 0
    for community in community_list:
        df = community_linkstream(link_streams,community)
        deltadensity_list += delta_density_list(df,d,tspan)
        delta_list += d
        community_id += list(np.repeat(count, len(d)))
        print(count)
        count += 1
    data = pd.DataFrame({'delta': delta_list, 'density': deltadensity_list, 'community_id': community_id})
    sns.lmplot(x='delta',y='density',data=data, hue='community_id',fit_reg=False,sharex=False,sharey=False)
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    plt.show()

def plot_max_deltadensity_delta(link_streams,community_list) :
    """
    Plot the distribution of max delta-density with smallest delta where delta-density is max.
    :param link_streams: pandas dataframe consist of t (timestamp), u (node that interact with v), v (node that interact with u).
    :param community_list: list of community eg. [[1,2,4],[3,5]].
    :return: void
    """
    delta_list = []
    density_list = []
    for community in community_list :
        list_max = max_stream_deltadensity(link_streams,community)
        delta_list.append(list_max[0])
        density_list.append(list_max[1])
    data = pd.DataFrame({'delta':delta_list,'density':density_list})
    sns.jointplot(x='delta',y='density',data=data)
    plt.show()

def plot_deltadensity_characteristic_delta(link_streams,community_list) :
    delta_list = []
    density_list = []
    for community in community_list :
        c_delta = characteristic_delta(link_streams,community)
        delta_list.append(c_delta[0])
        density_list.append(c_delta[1])
    data = pd.DataFrame({'delta': delta_list, 'density': density_list})
    diff = np.diff([density_list, delta_list])
    sns.jointplot(x='delta', y='density', data=data)
    plt.show()

def clustering_dbscan_derivative_plot(deltadensity_result, eps, min_sample, n_diff=1):
    df = dbscan_derivative_clustering(deltadensity_result, eps, min_sample, n_diff=n_diff)
    tmp = df.drop(['community_id','group'], axis=1)
    delta_list = [int(i) for i in list(tmp.columns)]
    deltadensity_column = []
    delta_column = []
    group_column = []
    for i in range(0, len(deltadensity_result)):
        deltadensity_column += list(tmp.loc[i, ])
        delta_column += delta_list
        group_column += list(np.repeat(df.loc[i, ['group']], len(delta_list)))
    to_plot = pd.DataFrame({'delta': delta_column, 'deltadensity': deltadensity_column, 'group': group_column})
    group_list = list(np.unique(to_plot.group))
    # plt.figure(1)
    for group in group_list:
        # plt.subplot(group)
        sns.lmplot(x='delta', y='deltadensity', hue='group', data=to_plot.loc[to_plot.group == group], fit_reg=False)
    plt.show()

def clustering_dbscan_deltadensity_plot(deltadensity_result, eps, min_sample):
    df = dbscan_delta_density_clustering(deltadensity_result, eps, min_sample)
    tmp = df.drop(['community_id','group'], axis=1)
    delta_list = [int(i) for i in list(tmp.columns)]
    deltadensity_column = []
    delta_column = []
    group_column = []
    for i in range(0, len(deltadensity_result)):
        deltadensity_column += list(tmp.loc[i, ])
        delta_column += delta_list
        group_column += list(np.repeat(df.loc[i, ['group']], len(delta_list)))
    to_plot = pd.DataFrame({'delta': delta_column, 'deltadensity': deltadensity_column, 'group': group_column})
    group_list = list(np.unique(to_plot.group))
    # plt.figure(1)
    for group in group_list:
        # plt.subplot(group)
        sns.lmplot(x='delta', y='deltadensity', hue='group', data=to_plot.loc[to_plot.group == group], fit_reg=False)
    plt.show()

def clustering_kmeans_derivative_plot(deltadensity_result, n_cluster, n_diff=1):
    df = kmeans_derivative_clustering(deltadensity_result, n_cluster=n_cluster, n_diff=n_diff)
    tmp = df.drop(['community_id', 'group'], axis=1)
    delta_list = [int(i) for i in list(tmp.columns)]
    deltadensity_column = []
    delta_column = []
    group_column = []
    for i in range(0, len(deltadensity_result)):
        deltadensity_column += list(tmp.loc[i,])
        delta_column += delta_list
        group_column += list(np.repeat(df.loc[i, ['group']], len(delta_list)))
    to_plot = pd.DataFrame({'delta': delta_column, 'deltadensity': deltadensity_column, 'group': group_column})
    group_list = list(np.unique(to_plot.group))
    # plt.figure(1)
    for group in group_list:
        # plt.subplot(group)
        sns.lmplot(x='delta', y='deltadensity', hue='group', data=to_plot.loc[to_plot.group == group], fit_reg=False)
    plt.show()

def clustering_kmeans_deltadensity_plot(deltadensity_result, n_cluster):
    df = kmeans_deltadensity_clustering(deltadensity_result, n_cluster=n_cluster)
    tmp = df.drop(['community_id', 'group'], axis=1)
    delta_list = [int(i) for i in list(tmp.columns)]
    deltadensity_column = []
    delta_column = []
    group_column = []
    for i in range(0, len(deltadensity_result)):
        deltadensity_column += list(tmp.loc[i,])
        delta_column += delta_list
        group_column += list(np.repeat(df.loc[i, ['group']], len(delta_list)))
    to_plot = pd.DataFrame({'delta': delta_column, 'deltadensity': deltadensity_column, 'group': group_column})
    sns.lmplot(x='delta', y='deltadensity', hue='group', data=to_plot, fit_reg=False)
    plt.xlim([min(to_plot.delta), max(to_plot.delta)])
    plt.ylim([0, 1])
    plt.show()

def linkstream_plot(linkstream):
    plt.axes()
    for i in range(0,len(linkstream)):
        line = plt.Line2D((linkstream.loc[i,'t'],linkstream.loc[i,'t']), (linkstream.loc[i,'u'],linkstream.loc[i,'v']), marker='.', markersize=10, color='black')
        plt.gca().add_line(line)
    plt.xlim([-1,max(linkstream.t)])
    plt.ylim([-1,max(linkstream.u)])
    plt.show()


def deltadensity_derivative_linkstream_plot(linkstream, community,start_delta=-1,stop_delta=-1,step=1):
    linkstream_community = community_linkstream(linkstream, community)
    fig = plt.figure(figsize=(8,8))
    axes = [fig.add_subplot(4,1,1),fig.add_subplot(4,1,2),fig.add_subplot(4,1,3)]

    tspan = max(linkstream.t) + 1
    start = 0
    stop = tspan - 1
    if start_delta != -1: start = start_delta
    if stop_delta != -1: stop = stop_delta
    seq_deltadensity = community_deltadensity_sequence(link_streams=linkstream_community, community=community, range=tspan,
                                                       start_delta=start, stop_delta=stop, step=step)
    deltadensity_df = pd.DataFrame({'delta': seq_deltadensity['delta'], 'density': seq_deltadensity['density']})
    second_derivative = np.diff(seq_deltadensity['density'], n=2)
    second_derivative_df = pd.DataFrame({'id': seq_deltadensity['delta'][0:-2], 'second_derivative': second_derivative})

    sns.regplot(x='delta', y='density', data=deltadensity_df, ax=axes[0], fit_reg=False)
    sns.regplot(x='id', y='second_derivative', data=second_derivative_df, ax=axes[1], fit_reg=False,)

    # line = plt.Line2D((1,1600000),(0,0.8))
    # axes[2].add_line(line)

    for i in range(0, len(linkstream_community)):
        line = plt.Line2D((linkstream_community.loc[i, 't'], linkstream_community.loc[i, 't']),
                          (linkstream_community.loc[i, 'u'], linkstream_community.loc[i, 'v']), marker='.', markersize=10, color='black')
        axes[2].add_line(line)

    [ax.autoscale_view() for ax in axes]

    axes[2].set_xlim([min(linkstream.t),max(linkstream.t)])

    plt.show()

def dl_stat_linkstream_plot(linkstream, community,start_delta=-1,stop_delta=-1,step=1, block = True):
    linkstream_community = community_linkstream(linkstream, community)
    fig = plt.figure(figsize=(8,8))
    axes = [fig.add_subplot(2,1,1),fig.add_subplot(2,1,2)]

    tspan = max(linkstream.t) + 1
    start = 0
    stop = tspan - 1
    if start_delta != -1: start = start_delta
    if stop_delta != -1: stop = stop_delta
    seq_deltadensity = community_deltadensity_sequence(link_streams=linkstream_community, community=community, range=tspan,
                                                       start_delta=start, stop_delta=stop, step=step)
    deltadensity_df = pd.DataFrame({'delta': seq_deltadensity['delta'], 'density': seq_deltadensity['density']})
    second_derivative = list(np.diff(seq_deltadensity['density'], n=2))
    second_derivative = [0] + second_derivative + [0]

    second_derivative_df = pd.DataFrame({'delta': seq_deltadensity['delta'], 'second_derivative': second_derivative })

    sns.pointplot(x='delta', y='density', data=deltadensity_df, ax=axes[0], fit_reg=False, color='black', join=False)
    sns.pointplot(x='delta', y='second_derivative', data=second_derivative_df, ax=axes[0], color='red')

    for i in range(0, len(linkstream_community)):
        line = plt.Line2D((linkstream_community.loc[i, 't'], linkstream_community.loc[i, 't']),
                          (linkstream_community.loc[i, 'u'], linkstream_community.loc[i, 'v']), marker='.', markersize=10, color='black')
        axes[1].add_line(line)

    [ax.autoscale_view() for ax in axes]

    axes[1].set_xlim([min(linkstream.t),max(linkstream.t)])

    plt.show(block= block)


data = get_input(link_streams_path='../data/board/linkstream.csv',communities_path='../data/board/communities.json')


# plot_max_deltadensity_delta(data['linkstream'],data['community'])
# for i in range(0,1):
#     plot_seq_community_deltadensity(link_streams=data['linkstream'],community=data['community'][i],start_delta=3600,stop_delta=604800,step=7200)
# plot_seq_communities_deltadensity(link_streams=data['linkstream'],community_list=data['community'],start_delta=3600,stop_delta=604800,step=7200)

# data = get_input('../data/board/linkstream.csv','../data/board/communities.json')
# community = list(np.unique(data['linkstream'].loc[:, ['u', 'v']]))
# print(data['linkstream'])
# plot_max_deltadensity_delta(data['linkstream'],data['community'])
# plot_deltadensity_characteristic_delta(data['linkstream'],data['community'])
# plot_seq_community_deltadensity(data['linkstream'],community, start_delta=3600, stop_delta=int(max(data['linkstream'].t)),step=7200)

# plot_seq_community_deltadensity(data['linkstream'],data['community'][19], start_delta=3600, stop_delta=1200000, step = 7200)
result = read_csv('../data/delta_density_result/result_for_clustering.csv')
clustering_dbscan_deltadensity_plot(result, eps=1, min_sample=2)
clustering_dbscan_derivative_plot(result, eps=0.0095, min_sample=2, n_diff=2)
# clustering_kmeans_deltadensity_plot(result, n_cluster=2)
# clustering_kmeans_derivative_plot(result, n_cluster=3)
# linkstream_plot(linkstream=data['linkstream'])
# print(min(data['linkstream'].t))
# print(max(data['linkstream'].t))


# dl_stat_linkstream_plot(data['linkstream'],data['community'][2],start_delta=3600, stop_delta=max(data['linkstream'].t), step=86400, block=False) # 2, 8, 70
# dl_stat_linkstream_plot(data['linkstream'],data['community'][8],start_delta=3600, stop_delta=max(data['linkstream'].t), step=86400, block=False) # 2, 8, 70
# dl_stat_linkstream_plot(data['linkstream'],data['community'][70],start_delta=3600, stop_delta=max(data['linkstream'].t), step=86400) # 2, 8, 70