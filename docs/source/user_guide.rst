User Guide
==========


This user guides aims to help new users of the Cryptographic Estimator library to quickly start with their estimations.

Using this library
==================

.. doctest::

    >>> from cryptographic_estimators.SDEstimator import SDEstimator
    >>> from cryptographic_estimators.SDEstimator.SDAlgorithms import BJMMdw
    >>> A = SDEstimator(3488,2720,64,excluded_algorithms=[BJMMdw],memory_access=1)
    >>> A.table(precision=3, show_all_parameters=1)
    +---------------+--------------------------------------------------------------------------------+
    |               |                                    estimate                                    |
    +---------------+---------+---------+------------------------------------------------------------+
    | algorithm     |    time |  memory |                         parameters                         |
    +---------------+---------+---------+------------------------------------------------------------+
    | BallCollision | 157.098 |  49.814 |             {'r': 7, 'p': 4, 'pl': 0, 'l': 39}             |
    | BJMMpdw       | 149.859 |  76.469 |            {'r': 7, 'p': 10, 'p1': 7, 'w2': 0}             |
    | BJMM          | 148.587 | 104.057 | {'r': 7, 'depth': 3, 'p': 16, 'p1': 6, 'p2': 12, 'l': 197} |
    | BothMay       | 148.170 |  87.995 |   {'r': 7, 'p': 12, 'w1': 0, 'w2': 0, 'p1': 9, 'l': 79}    |
    | Dumer         | 157.030 |  49.895 |                 {'r': 7, 'l': 39, 'p': 4}                  |
    | MayOzerov     | 147.232 |  86.592 | {'r': 7, 'depth': 3, 'p': 12, 'p1': 5, 'p2': 10, 'l': 95}  |
    | Prange        | 177.819 |  21.576 |                          {'r': 7}                          |
    | Stern         | 157.047 |  49.814 |                 {'r': 7, 'p': 4, 'l': 39}                  |
    +---------------+---------+---------+------------------------------------------------------------+


Optimizing under memory constraints
-----------------------------------



Adding a new Algorithm to an existing Estimator
===============================================

Lets add a new algorithm to an existing estimator.



Adding new Estimator
====================

To add a whole new estimator:


Examples (Please Ignore, this is just for testing)
==================================================


.. This is a comment.


**Lumache** (/lu'make/) is a Python library for cooks and food lovers that
creates recipes mixing random ingredients.  It pulls data from the `Open Food
Facts database <https://world.openfoodfacts.org/>`_ and offers a *simple* and
*intuitive* API.

.. note::

   This project is under active development.



Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.
