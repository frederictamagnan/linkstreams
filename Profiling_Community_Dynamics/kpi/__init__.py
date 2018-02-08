# Author: Frederic Tamagnan
# Date: 27 february 2017
# Licence: under the EUPL V.1.1




import Profiling_Community_Dynamics as pcd
import matplotlib.pyplot as plt
import Profiling_Community_Dynamics.static_graph as sg



def average_incident_degrees(linkstream, start_time=None, end_time=None):
	"""
	compute the mean of the incident edges on each vertex, in a slice of the linkstream defined by a start time and an end time
		
	:param linkstream: the linkstream concerned
	:param start_time: start time of the slice of the linkstream
	:param end_time: end time of the slice of the linkstream
	:return: a float, result of the compute
	"""	  

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])

	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]
	return df.groupby("v").size().mean()

def average_nonincident_degrees(linkstream, start_time=None, end_time=None):
	"""
	compute the mean of the nonincident edges on each vertex, edges which leave the vertex, in a slice of the linkstream defined by a start time and an end time
		
	:param linkstream: the linkstream concerned
	:param start_time: start time of the slice of the linkstream
	:param end_time: end time of the slice of the linkstream
	:return: a float, result of the compute
	"""	

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])

	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]
	return df.groupby("u").size().mean()


def number_of_interactions(linkstream , start_time=None, end_time=None):
	"""
	compute number of interactions, in a slice of the linkstream defined by a start time and an end time

	:param linkstream: the linkstream concerned
	:param start_time: start time of the slice of the linkstream
	:param end_time: end time of the slice of the linkstream
	:return: a float, result of the compute
	"""	

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])
	
	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]

	return df['u'].size



def average_delta_timestamp(linkstream, start_time=None, end_time=None):
	"""
	compute the average time between two edges in a slice of the linkstream defined by a start_time and a end_time

	:param linkstream: the linkstream concerned
	:param start_time: start time of the slice of the linkstream
	:param end_time: end time of the slice of the linkstream
	:return: a float, result of the compute
	"""	

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])
	
	df = df.loc[(df.loc[:, linkstream.column_timestamp] >= start_time) & (df.loc[:, linkstream.column_timestamp] <= end_time),]


	somme=end_time- start_time
	liste=df['t'].values.tolist()
	nombre = len(liste)-1
	
	return somme/nombre


def vizualisation_kpi (linkstream, start_time=None, end_time=None, func=number_of_interactions, step=1, delta=10):
	"""
	vizualisation of the evolution of a kpi on a slice of the linkstream defined by a start_time and an end_time. Each point is the compute of the kpi on a slice with a length of delta
    :param linkstream: the linkstream concerned
    :param start_time: start time of the slice of the linkstream
    :param end_time: end time of the slice of the linkstream
    :param func: the kpi to vizualise
    :param step: step of computing, time between each point
    :param delta: length of the portion of linkstream the compute will be done on
    :return : returns nothing but plot the evolution


	"""

	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])


	iterator =start_time
	y=[]
	x=[]


	while iterator<end_time:
		x.append(iterator)
		y.append(func(linkstream,iterator,iterator+delta))
		iterator=iterator+step


	plt.plot(x,y,)
	plt.ylabel(func.__name__)
	plt.xlabel("time")



def vizualisation_all_kpi(linkstream, start_time=None, end_time=None, step=1, delta=10):
	"""
	vizualisation of the four KPI on a slice off the linkstream defined by a start_time and an end_time. Each point is the compute of the kpi on a slice with a length of delta
    :param linkstream: the linkstream concerned
    :param start_time: start time of the slice of the linkstream
    :param end_time: end time of the slice of the linkstream
    :param step: step of computing, time between each point
    :param delta: length of the portion of linkstream the compute will be done on
    :return : returns nothing but plot the evolution


	"""

	#list of all kpi function
	liste_func=[average_incident_degrees,average_nonincident_degrees, number_of_interactions,average_delta_timestamp]
	liste_color=['r','b','y','g']
	#define the start time and the end time of the plot
	ls=linkstream
	df=linkstream.linkstream

	if start_time is None: # If start_time is not assigned, it is assigned to be first timestamp in linkstream.
	   	start_time = min(df.loc[:, linkstream.column_timestamp])
	if end_time is None: # If end_time is not assigned, it is assigned to be last timestamp in linkstream.
		end_time = max(df.loc[:, linkstream.column_timestamp])

	
	fig=plt.figure(1)
	st= fig.suptitle("DASHBOARD", fontsize="x-large")

	for i,func in enumerate(liste_func):
		iterator =start_time
		y=[]
		x=[]

		while iterator<end_time:
			x.append(iterator)
			y.append(func(linkstream,iterator,iterator+delta))
			iterator=iterator+step

		plt.subplot(len(liste_func),1,i+1)
		plt.plot(x,y,liste_color[i])
		plt.title(func.__name__+" in function of time")
		#plt.xlabel("time")



	plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=0.7)
	st.set_y(0.95)
	fig.subplots_adjust(top=0.85)

	"""
	fig2=plt.figure(2)
	sg.ls_flat_plot(ls)
	fig3=plt.figure(3)
	pcd.lsplot(ls)
	"""


"""
ls=gen.generator(edges=30)

vizualisation_all_kpi(ls,delta=60,step=20)

plt.show()
"""
