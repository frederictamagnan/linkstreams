Profiling_Community_Dynamics package
====================================

Subpackages
-----------

.. toctree::

    Profiling_Community_Dynamics.computation_module
    Profiling_Community_Dynamics.visualization_module

Module contents
---------------

.. automodule:: Profiling_Community_Dynamics
    :members:
    :undoc-members:
    :show-inheritance:

Example
-------
Creating LinkStream object
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can create the linkstream by

.. code-block:: python

    import Profiling_Community_Dynamics as pcd

    ls = pcd.LinkStream(data=[(1,2,3),(2,3,4),(3,4,5)])

Inside the tuple, the element are sender_id, receiver_id, and timestamp respectively.

When you create the LinkStream object by the code above, it will create the `Pandas Dataframe <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`_ and set column name of sender, receiver, and timestamp as 'u', 'v', and 't'.

If you would link to use a different column name, you can specify a column name like this

.. code-block:: python

    ls = pcd.LinkStream(data=[(1,2,3),(2,3,4),(3,4,5)], column_sender='sender',
                    column_receiver='receiver', column_timestamp='timestamp')

If you have the file of linkstream in CSV format, you can import your file to create LinkStream object by

.. code-block:: python

    ls = pcd.read_linkstream(path='./data/example/linkstream.csv')

Ofcourse, the default of column name is still u(sender), v(receiver), t(timestamp). you can specify the column name by the same way as creating LinkStream object.

.. code-block:: python

    ls = pcd.read_linkstream(path='./data/board/linkstream.csv', column_sender='authorA', column_receiver='authorB', column_timestamp='time')

Usage of LinkStream object
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can generate every possible community in the linkstream by

.. code-block:: python

    ls.generate_communities()

and then, it will return you a list of communities like this

.. code-block:: python

    [
        (1, 2), 
        (1, 3), 
        (1, 4), 
        (1, 5), 
        (2, 3), 
        (2, 4), 
        (2, 5), 
        (3, 4), 
        (3, 5), 
        (4, 5), 
        (1, 2, 3), 
        (1, 2, 4), 
        (1, 2, 5), 
        (1, 3, 4), 
        (1, 3, 5), 
        (1, 4, 5), 
        (2, 3, 4), 
        (2, 3, 5), 
        (2, 4, 5), 
        (3, 4, 5), 
        (1, 2, 3, 4), 
        (1, 2, 3, 5), 
        (1, 2, 4, 5), 
        (1, 3, 4, 5), 
        (2, 3, 4, 5), 
        (1, 2, 3, 4, 5)
    ]

Inside the list, tuple refers to one community and the element inside a tuple is id of node which is in that community.

In addition, you can describe the linkstream by

.. code-block:: python

    ls.describe()

the console will show you like this

.. code-block:: python

    Nodes: [1, 2, 3, 4, 5]
    Number of node: 5
    Number of link: 36
    Timestamp: 
    count    24.000000
    mean     23.458333
    std      13.516429
    min       2.000000
    25%      10.750000
    50%      25.000000
    75%      34.250000
    max      43.000000
    dtype: float64
    Timerange: 
    count    23.000000
    mean      1.782609
    std       0.951388
    min       1.000000
    25%       1.000000
    50%       2.000000
    75%       2.000000
    max       4.000000
    dtype: float64

and return statistic of node list, timestamp list which link is occured, and timerange between two near timestamp list.

.. code-block:: python

   {
        'timestamp_list': 
        count    24.000000
        mean     23.458333
        std      13.516429
        min       2.000000
        25%      10.750000
        50%      25.000000
        75%      34.250000
        max      43.000000
        dtype: float64, 
        'node_list': 
        count    5.000000
        mean     3.000000
        std      1.581139
        min      1.000000
        25%      2.000000
        50%      3.000000
        75%      4.000000
        max      5.000000
        dtype: float64, 
        'timerange_list': 
        count     7.000000
        mean      2.714286
        std      10.181205
        min     -11.516429
        25%      -5.241786
        50%       8.750000
        75%       9.000000
        max      14.250000
        dtype: float64
    }


If you do not want the console show the statistic, you can set parameter display as False.

.. code-block:: python

    ls.describe(display=False)

and it just return values.