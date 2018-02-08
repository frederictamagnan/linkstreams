kpi module
====================================

Module contents
---------------

.. automodule:: kpi
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
Creating LinkStream object
^^^^^^^^^^^^^^^^^^^^^^^^^^
first we create a linkstream with

.. code-block:: python

    import Profiling_Community_Dynamics as pcd
    import matplotlib.pyplot as plt

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')
    pcd.lsplot(ls)
    plt.show()

.. image:: kpi_linkstream.png

Computation of a kpi
^^^^^^^^^^^^^^^^^^^^^^^^^^
then we compute a kpi


.. code-block:: python
    
    n=pcd.number_of_interactions(ls)
    print(n)
    
Dashboard - summary of all kpis
^^^^^^^^^^^^^^^^^^^^^^^^^^
then we can plot a dashboard of a linkstream

.. code-block:: python
    
    pcd.vizualisation_all_kpi(ls)
    plt.show()

and the result is

.. image:: kpi_dashboard.png
