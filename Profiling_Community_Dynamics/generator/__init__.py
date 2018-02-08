# Author: Frederic Tamagnan
# Date: 27 february 2017
# Licence: under the EUPL V.1.1





import Profiling_Community_Dynamics as pcd
import matplotlib.pyplot as plt
import random as rm
import networkx as nx
import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np


import sys
import os

sys.path.append(str(os.getcwd()) + '../Profiling_Community_Dynamics')
sys.path.append(str(os.getcwd()) + '../Profiling_Community_Dynamics/visualization_module')
sys.path.append(str(os.getcwd()) + '../Profiling_Community_Dynamics/computation_module')


def matrix_prob_creation (size_pop=12,nb_cluster=2, size_cluster_equal= True, high_prob=0.9,low_prob=0.1 ):
    """
    Generate a matrix which represents the probability to establish a link between people in a linkstream
    You can choose  an equal repartition in each cluster or a random repartition
	
    :param size_pop: the number of people in the population
    :param nb_cluster: the number of clusters
    :param size_cluster_equal: if you want the same number of people in your clusters of not
    :param high_prob: the probability to establish a link between two people in the same cluster.
    :param low_prob: the probability to establish a link between two people in two differents cluster
    """
	
    #initialize a matrix with zeros
    matrix=np.zeros((size_pop,size_pop))


    liste_size=[]

    #define a liste_size
    if size_cluster_equal:
        i=0
        while i< nb_cluster:
                liste_size.append(size_pop//nb_cluster)
                i=i+1
        liste_size.append(size_pop-sum(liste_size))
		#print(liste_size)
    else:# ---> repartition of the population in each cluster randomly
        i=1
        liste_size.append(rm.randint(1,size_pop-1))
        while i<nb_cluster-1 and sum(liste_size)<size_pop:
                liste_size.append(rm.randint(0,size_pop-sum(liste_size)))
                i=i+1
        liste_size.append(size_pop-sum(liste_size))

    """
	browse the matrix with control structure to know if row and column are in the same cluster or not
	i = iterator inside a cluster
	iterator_row = iterator to pass from a cluster to another for the rows
	elt_row = the size of each cluster
    """
    for iterator_row,elt_row in enumerate(liste_size):
        i=0
        while i<elt_row:
                row=i+sum(liste_size[:iterator_row])
                for iterator_column,elt_column in enumerate(liste_size):
                        j=0
                        while j<elt_column:
                                column = j + sum(liste_size[:iterator_column])
                                if iterator_column== iterator_row:
                                        matrix[row][column]=high_prob
                                else:
                                        matrix[row][column]=low_prob
                                j=j+1
                i=i+1
    return matrix
		

def generator(matrix=None,size_pop=10,edges=30,mathfunc=lambda x: rm.randint(0,10)):
        """
        Generate a linkstream from a matrix of probabilities of interaction

        :param matrix: the matrix of probabilities of interaction
        :param size_pop: number of vertices in the linkstream
        :param edges: number of edges in the linkstream
        :param mathfunc: the mathematical function that will compute the time between two edges
        
        :return: a linkstream randomly generated
        """
	
	#define a matrix of probabilities of an edge between two vertices
        if matrix is None:
                matrix=np.random.random((size_pop,size_pop))
        else:
                size_pop= np.size(matrix,1)

        i=0
        liste_edges=[]
        timestamp=0
        while i<edges:
                u=rm.randint(0,size_pop-1)
                v=u
                while v==u:
                        v=rm.randint(0,size_pop-1)

                if matrix[u][v]> rm.uniform(0,1):
                        liste_edges.append((u,v,timestamp))
                        i=i+1
                timestamp=timestamp+mathfunc(i)
                
	
        if len(liste_edges)==0:
                return None
        else:
                return pcd.LinkStream(liste_edges)

"""
matrix= matrix_prob_creation()

ls=generator(matrix=matrix)
g=convert_linkstream_to_nx_graph(ls)

pcd.lsplot(ls)
plt.show()
nx.draw(g)
plt.show()

"""
