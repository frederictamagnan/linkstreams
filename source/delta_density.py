import numpy as np

def links_deltadensity(link_stream, delta, tspan) :

    """
    :param link_stream: pandas dataframe that consist of column t (int: the timestamp of link), u (int: the id of node), v (int: the id of node).
    :param delta: float The time duration that you want to compute the delta-density.
    :param tspan: float The range of start timestamp and last timestamp.
    :return: float The delta-density of link.
    """

    t_init = 0
    links_dict = {}
    links_deltadensity = {}
    for i in range(0,len(link_stream)):
        link = frozenset([link_stream.at[i,'u'],link_stream.at[i,'v']])
        if links_dict.get(link) is None :
            links_dict[link] = [t_init,0,1]
        if links_dict[link][2] == 1 :
            links_dict[link][1] += max((link_stream.at[i,'t'] - t_init) - delta,0)
        else :
            links_dict[link][1] += max((link_stream.at[i,'t'] - links_dict[link][0]) - delta,0)
        links_dict[link][2] += 1
        links_dict[link][0] = link_stream.at[i,'t']
    for link in links_dict :
        links_dict[link][1] += max((tspan - links_dict[link][0]) - delta,0)
        links_deltadensity[link] = 1 - float(links_dict[link][1])/(tspan - delta)
    return links_deltadensity

def stream_deltadensity(link_stream, delta, tspan) :

    """
    :param link_stream: pandas dataframe that consist of column t (int: the timestamp of link), u (int: the id of node), v (int: the id of node).
    :param delta: float The time duration that you want to compute the delta-density.
    :param tspan: float The range of start timestamp and last timestamp.
    :return: float The delta-density of stream.
    """
    if link_stream.empty :
        return 0

    node_amount = len(np.unique(link_stream[['u','v']].values))
    link_deltadensity = links_deltadensity(link_stream, delta, tspan)
    sum_links_deltadensity = 0
    for link, link_density in link_deltadensity.items() :
        sum_links_deltadensity += link_density
    return (2 * sum_links_deltadensity / ((node_amount)*(node_amount - 1)))


def delta_density_list(link_stream, delta_list, tspan):
    """
    :param link_stream:
    :param delta:
    :param tspan:
    :return:
    """
    density_list = []
    for delta in delta_list:
        density_list.append(stream_deltadensity(link_stream,delta,tspan))

    return density_list

from pandas.io.parsers import read_csv

df = read_csv('../data/example/linkstream.csv')
print(links_deltadensity(df, 1, 44))
