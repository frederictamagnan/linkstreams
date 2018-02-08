# Author: Patipol Chiammunchit
# Date: 22 July 2016
# Licence: under the EUPL V.1.1
# Inspiration: https://www-complexnetworks.lip6.fr/~magnien/DynGraph/Software/Delta_Density/

import sys
import os

sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/visualization_module')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/computation_module')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/Entropy')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/generator')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/kpi')
sys.path.append(str(os.getcwd()) + '/Profiling_Community_Dynamics/static_graph')

from pandas.io.parsers import read_csv
from Profiling_Community_Dynamics.visualization_module import *
from Profiling_Community_Dynamics.computation_module import *
from Profiling_Community_Dynamics.Entropy import *
from Profiling_Community_Dynamics.generator import *
from Profiling_Community_Dynamics.kpi import *
from Profiling_Community_Dynamics.static_graph import *
import numpy as np
import itertools
import pandas as pd


def read_linkstream(path, column_sender='u', column_receiver='v', column_timestamp='t'):
    """
    Import .csv file to LinkStream Object.

    :param path: A path of the linkstream file(.csv).
    :param column_sender: A name of sender column.
    :param column_receiver: A name of receiver column.
    :param column_timestamp: A name of timestamp column.
    :return: A LinkStream object.
    """
    df = read_csv(path) # Use pandas package to import csv file
    ls = LinkStream( # Create LinkStream object
        data={column_sender: list(df.loc[:, column_sender]), column_receiver: list(df.loc[:, column_receiver]),
              column_timestamp: list(df.loc[:, column_timestamp])}, column_sender=column_sender,
        column_receiver=column_receiver, column_timestamp=column_timestamp)
    return ls


class LinkStream:
    """
    The class which contains Linkstream for data experiment eg. computing delta-density or visualization.

    :param str column_sender: A name of sender column.
    :param str column_receiver: A name of receiver column.
    :param str column_timestamp: A name of timestamp column.
    :param data: List of tuple which contains 3 members, sender_id(int), receiver_id(int), timestamp(int).
    """

    def __init__(self, data, column_sender='u', column_receiver='v', column_timestamp='t'):

        self.linkstream = pd.DataFrame(data=data, columns=[column_sender, column_receiver, column_timestamp]) # Create pandas Data
        self.column_sender = column_sender
        self.column_receiver = column_receiver
        self.column_timestamp = column_timestamp
        self.linkstream = self.linkstream.sort_values([column_timestamp], ascending=['1'])

    def describe(self, display=True):
        """
        Describe the linkstream.

        :param display: print the describing of nodes, link, timestamp, etc.
        :return: map which contains node list, timestamp list, and time range list.
        """
        return_dict = {}
        return_dict['node_list'] = pd.Series(list(
            np.unique(self.linkstream.loc[:, [self.column_sender, self.column_receiver]].values))).describe() # add node_list statistic object in dictionary
        return_dict['timestamp_list'] = pd.Series(list(np.unique(self.linkstream.t))).describe() # add timestamp_list statistic object in dictionary
        sorted(return_dict['timestamp_list'])
        return_dict['timerange_list'] = pd.Series(list(np.diff(return_dict['timestamp_list']))).describe() # add timerange_list statistic object in dictionary
        if display:
            print("Nodes: %s" % str(return_dict['node_list']))
            print("Number of node: %d" % len(return_dict['node_list']))
            print("Number of link: %s" % len(self.linkstream))
            print("Timestamp: ")
            print(pd.Series(return_dict['timestamp_list']).describe())
            print("Timerange: ")
            print(pd.Series(return_dict['timerange_list']).describe())
        return return_dict

    def generate_communities(self):
        """
        Generate every possible community of the linkstream.

        :return: list of tuple of nodes in each community.
        """
        node_list = list(np.unique(self.linkstream.loc[:, [self.column_sender, self.column_receiver]].values)) # Get users in linkstream.
        communities = []
        for i in range(2, len(node_list) + 1): # Do combination of users for generating communities
            communities_list = list(itertools.combinations(node_list, i))
            communities += communities_list
        return communities
