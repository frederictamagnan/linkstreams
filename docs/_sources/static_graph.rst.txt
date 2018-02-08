static_graph module
====================================

Module contents
---------------

.. automodule:: static_graph
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------

These four function are based on the API https://networkx.github.io/ created to manipulate static graph.

Ls_flat_plot function
^^^^^^^^^^^^^^^^^^^^^

This function draw a flat instance of a linkstream. If a link appears two times during the linkstream, only one link is represented on the flat graph


.. code-block:: python

    import Profiling_Community_Dynamics as pcd
    matrix_1= pcd.matrix_prob_creation(size_pop=20,nb_cluster=3, size_cluster_equal= True, high_prob=0.9,low_prob=0)
    ls1=pcd.generator(edges=30,matrix=matrix_1)
    import matplotlib.pyplot as plt
    pcd.ls_flat_plot(ls1)
    plt.show()
    



.. image:: static_graph_lsflatplot.png

Convert_networkx_to_linkstream function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function convert a networkx instance to a linkstream, by attaching a timestamp randomly to each edge.

.. code-block:: python

     import Profiling_Community_Dynamics as pcd
     import networkx as nx
     import matplotlib.pyplot as plt
     
     static_graph=nx.erdos_renyi_graph(3,0.5)
     #generate an erdos renyi graph with three vertex and a probability of 50% of interaction
     
     nx.draw(static_graph)
     plt.show()



.. image:: static_graph_nx_plot.png

then
     
.. code-block:: python

     ls= pcd.convert_networkx_to_linkstream(static_graph,mathfunc=lambda x: 1)
     #the length between two timestamp is set up to 1

     pcd.lsplot(ls)
     plt.show()


.. image:: static_graph_nx_plot2.png

     
Convert_linkstream_to_networkx function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^     

This function convert a linkstream to a networkx instance from the list of edges

.. code-block:: python
  
     import Profiling_Community_Dynamics as pcd
     import networkx as nx
     import matplotlib.pyplot as plt

     ls=pcd.generator()
     pcd.lsplot(ls)
     plt.show()

.. image:: static_graph_nx_plot3.png

.. code-block:: python

     graph=pcd.convert_linkstream_to_networkx(ls)
     nx.draw(graph)
     plt.show()   

.. image:: static_graph_nx_plot4.png

Nx_complex_generator function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



1) It takes the graph passed in parameter or generates a static erdos renyi graph 
2) It takes randomly an edge of this static graph and attaches a timestamp
3) until we reach the number of edges given at the beginning

if there is no networkx graph in parameter it will take by default the erdos renyi random graph generator to generate a linkstream
https://networkx.readthedocs.io/en/stable/reference/generators.html#module-networkx.generators.random_graphs

.. code-block:: python
  
     import Profiling_Community_Dynamics as pcd
     import networkx as nx
     import matplotlib.pyplot as plt

     ls=pcd.nx_complex_generator(n=10,p=0.7,edges=30)
     pcd.lsplot(ls)
     plt.show()

.. image:: static_graph_nx_erdos.png


.. code-block:: python
  
     import Profiling_Community_Dynamics as pcd
     import networkx as nx
     import matplotlib.pyplot as plt
     
     graph_karate= nx.karate_club_graph()
     ls=pcd.nx_complex_generator(edges=30,graph=graph_karate)
     pcd.lsplot(ls)
     plt.show()

.. image:: static_graph_nx_karate.png

