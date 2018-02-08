Profiling_Community_Dynamics.computation_module package
=======================================================

Module contents
---------------

.. automodule:: Profiling_Community_Dynamics.computation_module
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
links_deltadensity function
^^^^^^^^^^^^^^^^^^^^^^^^^^^
links_deltadensity is a function which compute the link delta-density of every possible pair of nodes.

The way to use this function is

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')
    pcd.links_deltadensity(ls, delta=1)

and the result will show you like this

.. code-block:: python

    {
        frozenset([2, 4]): 0.09523809523809523, 
        frozenset([1, 2]): 0.26190476190476186, 
        frozenset([1, 4]): 0.023809523809523836, 
        frozenset([3, 5]): 0.023809523809523836, 
        frozenset([3, 4]): 0.1428571428571429,
    }

You can specify the time of a linkstream by assign the value to parameter start_time and end_time like this

.. code-block:: python

    pcd.links_deltadensity(ls, delta=1, start_time=10, end_time=20)

Then, the function will compute the delta-density from link which is in duration of start_time and end_time.

Moreover, you can specify the community too by assign list of node id to parameter community.

.. code-block:: python

    pcd.links_deltadensity(ls, delta=1, community=[3,4,5])

It will compute the delta-density from link which occur from nodes in community.

stream_deltadensity function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function uses to compute delta-density of link stream.

.. code-block:: python

    pcd.stream_deltadensity(ls, delta=1)

and it will return delta-density of linkstream

.. code-block:: python

    0.08095238095238096

The same as links_deltadensity function, you can specity duration of time by assigning parameter start_time and end_time.

.. code-block:: python

    pcd.stream_deltadensity(ls, delta=1, start_time=10, end_time=20)

you can assign community which you would like to compute delta-density too.

.. code-block:: python

    pcd.stream_deltadensity(ls, delta=1, community=[3,4,5])

delta_density_list function
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function is like calling stream_deltadensity() several time. It computes stream delta-density with a list of delta values.

.. code-block:: python

    pcd.delta_density_list(ls, delta_list=[1,2,3,4,5], start_time=10, end_time=20, community=[3,4,5])

max_deltadensity_min_delta function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This function will find the maximum delta-density of link stream and the smallest delta where delta-density is maximum.

.. code-block:: python

    pcd.max_deltadensity_min_delta(ls)

and it will return map which contains min_delta and max_deltadensity like this

.. code-block:: python

    {
        'min_delta': 31, 
        'max_deltadensity': 0.8
    }

You can specify the community, and duration of time which you would like to consider by

.. code-block:: python

    pcd.max_deltadensity_min_delta(ls, start_time=10, end_time=20, community=[3,4,5])