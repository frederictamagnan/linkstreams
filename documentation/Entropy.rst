Entropy module
====================================

Module contents
---------------

.. automodule:: Entropy
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
distEntropy function
^^^^^^^^^^^^^^^^^^^^
distEntropy is a function which compute the linkstream entropy from a start time to an end time. If none given, the function will compute the entropy of the whole linkstream.

The way to use this function is

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')

    print(pcd.distEntropy(ls))

and the result will show you the value of the linkstream entropy.

You can also use other parameters like start time and delta in order to compute the delta-entropy : 

.. code-block:: python

    print(pcd.distEntropy(ls, start = 15, delta = 10))


matrixComp function
^^^^^^^^^^^^^^^^^^^
matrixComp is a function which compares two probability matrices by their mean, mediane and the standard deviation of the linkstreams associated. 4444

.. code-block:: python

    import numpy as np
    import Profiling_Community_Dynamics as pcd

    mat1 = np.matrix([[0,1,0,0],[1,0,0,0],[0,0,0,0],[0,0,0,0]])
    mat2 = np.matrix([[0,0.5,0.5,0.5],[0.5,0,0.5,0.5],[0.5,0.5,0,0.5],[0.5,0.5,0.5,0]])
	
    pcd.matrixComp(mat1,mat2)

and the result will return you a list containing the mean, std deviation and mediane of the entropy of the linkstream created based on each matrix.


meanEntropy function
^^^^^^^^^^^^^^^^^^^^
meanEntropy is a function which compute the mean delta-Entropy of a linkstream :

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')


    print(pcd.meanEntropy(ls, delta = 10, step = 1))


vizualisation_entropy function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vizualisation_entropy is a function which plots the entropy evolution of a linkstream over time.

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')
	
    pcd.vizualisation_entropy(ls)

.. image:: vizualisation_entropy.png

So is the case for the delta-entropy :

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')
	
    pcd.vizualisation_entropy(ls, step = 1, startTime = 0, delta=10)

.. image:: vizualisation_delta_entropy.png
