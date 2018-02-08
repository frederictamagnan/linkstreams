# Use assertions to make your tests
# Use None for default values in function calls
# Write comments in functions : #Initialization #Computation #Plot etc.
# Functions of the module

generate_communities(data)
"""
data : linkstream
returns : a set of set of nodes
"""

read_communities(file, id=None, columns=None, header=False):
"""
id : string
columns : list of string (metadata)
header : boolean
file: a csv file
returns : a set of set of nodes
"""

density(data, time=None, source=None, dest=None, delta=1, frame_start=None, frame_end=None, nodes=None)
"""
data : dataFrame
time : string
source : string
dest : string
delta : int
frame_start : int
frame_end : int
nodes : a list of nodes
returns : a dataframe with columns set of node, delta, delta_density
"""

describe(data, display=True)
"""
Prints statistics about a linkstream (if display == True) and returns an object with attributes: users, links, ...
data : dataFrame
display : boolean
"""

lsplot(data)
"""
display a linkstream with seaborn or matplotlib
@todo define parameters
"""

densityplot(data,s)
"""
display stats about delta density for one or several communities
@todo define parameters which are similar to seaborn.lmplot parameters
"""

