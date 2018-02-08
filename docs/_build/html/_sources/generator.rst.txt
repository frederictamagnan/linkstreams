generator module
====================================

Module contents
---------------

.. automodule:: generator
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
Matrix_prob_creation function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

this function allows you to create a matrix of probabilites function with a control on various parameters (number of cluster, size of population,etc).



.. code-block:: python

    import Profiling_Community_Dynamics as pcd
    matrix_1= pcd.matrix_prob_creation(size_pop=20,nb_cluster=3, size_cluster_equal= False, high_prob=0.9,low_prob=0)
    #the size of the clusters are random
    matrix_2= pcd.matrix_prob_creation(size_pop=20,nb_cluster=10, size_cluster_equal= True, high_prob=0.9,low_prob=0)
    #the size of the clusters are equal

Generator function
^^^^^^^^^^^^^^^^^^

Then we generate a linkstream of 30 edges from these two matrix

.. code-block:: python

    ls1=pcd.generator(edges=30,matrix=matrix_1)
    ls2=pcd.generator(edges=30,matrix=matrix_2)
    

We can see the results of the two linkstream in a concrete way with a plot representation

.. code-block:: python

    import matplotlib.pyplot as plt
    pcd.lsplot(ls1)
    plt.show()
    pcd.lsplot(ls2)
    plt.show()

Linkstreams plot
^^^^^^^^^^^^^^^^^^
First linkstream with 3 clusters, 20 people, number of people different in each cluster : 

.. image:: generator_ls1.png

Second linkstream with 10 clusters, 20 people, number of people equal in each cluster :

.. image:: generator_ls2.png
