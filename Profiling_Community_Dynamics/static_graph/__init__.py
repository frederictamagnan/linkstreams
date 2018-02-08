# Author: Frederic Tamagnan
# Date: 27 february 2017
# Licence: under the EUPL V.1.1


import Profiling_Community_Dynamics as pcd
import random as rm
import networkx as nx

def ls_flat_plot(linkstream, start_time=None, end_time=None):
	"""
	Plot a slice of a linkstream as a static graph


    :param start_time: beginning of the slice
    :param end_time: end of the slice
    :param linkstream: linkstream to plot
    :return: nothing but you can plot it with import matplotlib.pyplot as plt  plt.show()
	"""

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])

	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]

	linkstream.linkstream=df

	graph=convert_linkstream_to_networkx(linkstream)
	nx.draw(graph)




def convert_networkx_to_linkstream(graph,mathfunc= lambda x: rm.randint(0,10)):

	"""
    Import a newtworkx graph instance to LinkStream Object and compute the timestamp with a mathematical function.

    :param graph: a graph instance from the lib networkx
    :param mathfunc: a mathematical function to compute the difference between two interactions
    :return: A LinkStream object.
    """


	liste_edges=nx.to_edgelist(graph)
	timestamp=0
	data=[]
	data2=[]
	for i,elt in enumerate(liste_edges):
		data.append((elt[0],elt[1]))
	rm.shuffle(data)
	for i,elt in enumerate(data):
		data2.append((elt[0],elt[1],timestamp))
		timestamp=timestamp+mathfunc(i)
	return pcd.LinkStream(data2)



def convert_linkstream_to_networkx(linkstream,start_time=None, end_time=None):

	"""
    Import a slice of a LinkStream Object to a newtworkx graph instance 

    :param linkstream: a linkstream instance
    :param start_time: beginning of the slice
    :param end_time: end of the slice
    :return: A LinkStream object.
    """

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
		start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])

	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]

	liste_edges=list(zip(df.u, df.v))
	return nx.from_edgelist(liste_edges)


def nx_complex_generator(n=10,p=0.3,edges=30,graph= None, mathfunc=lambda x: rm.randint(0,10)):
	"""
    Generate a linkstream from a networkx graph (the default graph is a erdos renyi graph)

    :param n: number of vertices
    :param p: probability of interactions taken as parameter in the nxfunc
    :param edges: number of edges
    :param graph: a graph instance from the lib networkx
    :param mathfunc: a mathematical function to compute the difference between two interactions
    :return: A LinkStream object.
	"""
	if graph is None:
		nxfunc=nx.erdos_renyi_graph
		graph=nxfunc(n=n,p=p)


	timestamp=0
	data=[]
	data2=[]
	iterator=0

	
	liste_edges=nx.to_edgelist(graph)
	for i,elt in enumerate(liste_edges):
		data.append((elt[0],elt[1]))


	while iterator<edges:
		
		indice=rm.randint(0,len(data)-1)

		data2.append((data[indice][0],data[indice][1],timestamp))
		timestamp=timestamp+mathfunc(i)

		iterator=iterator+1

	return pcd.LinkStream(data2)


"""
ls=gen.generator()
ls_flat_plot(ls)
plt.show()
"""
