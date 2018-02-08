Profiling_Community_Dynamics.visualization_module package
=========================================================

Module contents
---------------

.. automodule:: Profiling_Community_Dynamics.visualization_module
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
lsplot function
^^^^^^^^^^^^^^^^
lsplot() is a function which visualizes a linkstream. X-axis is timestamp
and Y-axis is node id. You can plot a linkstream by

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')

    pcd.lsplot(ls)

and the result is

.. image:: lsplot_basic.png

You can specify the time of a linkstream by assign the value to parameter start_time and end_time like this

.. code-block:: python

    pcd.lsplot(ls, start_time=10, end_time=20)

Then, X-axis is fit start_time and end_time like this 

.. image:: lsplot_specific_time.png

Moreover, you can specify the community too by assign list of node id to parameter community.

.. code-block:: python

    pcd.lsplot(ls, community=[1,2,3])

It plot only link which is occured between node in parameter community.

.. image:: lsplot_specific_community.png

density_plot function
^^^^^^^^^^^^^^^^^^^^^

densityplot() is a function which visualizes the evolution of delta-density according to delta.

.. code-block:: python

    pcd.density_plot(ls)

X-axis is delta and Y-axis is delta-density. And, delta rises from 0 to whole time range of linkstream.

.. image:: density_plot_basic.png

If you would like to specify start delta and end delta, you can assign parameter start_delta and end_delta.

.. code-block:: python

    pcd.density_plot(ls, start_delta=5, end_delta=20)

.. image:: density_plot_specific_delta.png

By default, whole time range of linkstream is the timestamp of last link occured in linkstream (minus zero). Although, you can assign the whole time range of linkstream by assigning parameter start_time and end_time.

.. code-block:: python

    pcd.density_plot(ls, start_time=1, end_time=100)

.. image:: density_plot_specific_time.png

The same as lsplot, you can identify community which you would like to consider in parameter community.

.. code-block:: python

    pcd.density_plot(ls, community=[1,2,3])

.. image:: density_plot_specific_community.png

density_2nd_derivative_lsplot function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This function creates the figure which consists of the evolution of delta-density according to delta, second derivative of delta-density, and linkstream plot.

.. code-block:: python

    pcd.density_2nd_derivative_lsplot(ls)

.. image:: density_2nd_derivative_lsplot_basic.png

Setting parameter is like lsplot() and density_plot().

max_deltadensity_min_delta_plot function
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
The function creates the figure which X-axis refers to smallest delta where delta-density is maximum and Y-axis refers to the maximum delta-density of linkstream.

.. code-block:: python

    pcd.max_deltadensity_min_delta_plot(ls, communities=[(1,2), (1,4), (3,4,5)])

.. image:: max_deltadensity_min_delta_plot.png

This function also has parameter start_time and end_time and the way to use it is the same as lsplot(), density_plot(), and density_2nd_derivative_lsplot().