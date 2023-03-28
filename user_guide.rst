.. role:: bash(code)
   :language: bash


User Guide
==========

This library provides bit security estimators and asymptotic complexity estimators for cryptographic problems. So far it
covers the binary Syndrome Decoding Problem (SDEstimator), the Multivaritate Quadratic Problem (MQEstimator), the Linear
Code Equivalence Problem (LEEstimator), the Permutation Code Equivalence Estimator Problem (PEEstimator), the Permuted
Kernel Problem (PKEstimator) and the Syndrome Decoding Problem over Fq (SDFqEstimator).

Its build on top of `SageMath <https://sagemath.org>`_ and implemented using `Python3 <https://python.org>`_.

This user guides aims to help new users of the **Cryptographic Estimator** library to quickly start with their
estimations.

Installation
------------

Download the source from the git repository:

.. code-block:: bash

        git clone https://github.com/Crypto-TII/cryptographic_estimators
        cd cryptographic_estimators

From there on you can either install the package locally or use it via docker.

Local
^^^^^
First you need to install Sage. For this please follow this `online guide <https://doc.sagemath.org/pdf/en/installation/installation.pdf>`_.
Once you've Sage installed you can go to this project folder and run :bash:`make install` in a terminal. This will install
**cryptographic_estimators** library globally. If you encounter a permission error try again adding `sudo` as a
prefix, thus running :bash:`sudo make install`.

Docker
^^^^^^

If you don’t have sage installed in your machine you can start with our dockerized app. First you will need to have
running the DockerDesktop app or on the Linux the docker daemon and make sure that you are allowed to create docker
images as your local user. Refer to this `guide <https://docs.docker.com/get-started/overview/>`_ for help.

Finally you are able to execute

.. code-block:: bash

        make docker-build

or if you have an Apple Silicon M1 chip:

.. code-block:: bash

        make docker-build-m1

.. note::

   This process may take up to 15 or 20 minutes depending on your bandwidth and  computer capacity.

Quickstart
----------

Local
^^^^^
After successfully installing the library you can use it as a normal python library:

.. doctest::

    >>> from cryptographic_estimators.SDEstimator import SDEstimator
    >>> sd = SDEstimator(15,10,5)
    >>> sd.estimate()
    {'BallCollision': {'estimate': {'time': 9.579315937580013, 'memory': 8.60733031374961, 'parameters': {'r': 0, 'p': 2, 'pl': 0, 'l': 4}}, 'additional_information': {'permutations': 0, 'gauss': 4.643856189774724, 'lists': [3.321928094887362, 2.6438561897747244]}}, 'BJMMdw': {'estimate': {'time': 12.140510272368221, 'memory': 9.264442600226602, 'parameters': {'r': 0, 'p': 2, 'p1': 1, 'w1': 0, 'w11': 0, 'w2': 0}}, 'additional_information': {'constraints': [0, 2], 'permutations': 0, 'tree': 8.108524456778168, 'gauss': 4.643856189774724, 'representation': 4, 'lists': [2.321928094887362, 4.643856189774724, 7.287712379549449]}}, 'BJMMpdw': {'estimate': {'time': 12.140510272368221, 'memory': 9.264442600226602, 'parameters': {'r': 0, 'p': 2, 'p1': 1, 'w2': 0}}, 'additional_information': {'constraints': [0, 2], 'permutations': 0, 'tree': 8.108524456778168, 'gauss': 4.643856189774724, 'representation': 4, 'lists': [2.321928094887362, 4.643856189774724, 9.287712379549449]}}, 'BJMM': {'estimate': {'time': '--', 'memory': '--', 'parameters': {'r': 0, 'depth': 2}}, 'additional_information': {}}, 'BothMay': {'estimate': {'time': 8.714245517666122, 'memory': 7.076815597050831, 'parameters': {'r': 0, 'p': 2, 'w1': 0, 'w2': 0, 'p1': 5, 'l': 0}}, 'additional_information': {'constraints': [0], 'permutations': 0, 'tree': 1.584962500721156, 'gauss': 4.643856189774724, 'representation': 1, 'lists': [0.0, 0.0]}}, 'Dumer': {'estimate': {'time': 9.430452551665532, 'memory': 8.076815597050832, 'parameters': {'r': 0, 'l': 2, 'p': 1}}, 'additional_information': {'permutations': 0, 'gauss': 4.643856189774724, 'lists': [2.584962500721156, 3.169925001442312]}}, 'MayOzerov': {'estimate': {'time': '--', 'memory': '--', 'parameters': {'r': 0, 'depth': 2}}, 'additional_information': {}}, 'Prange': {'estimate': {'time': 13.550746785383243, 'memory': 6.491853096329675, 'parameters': {'r': 0}}, 'additional_information': {'permutations': 5.0, 'gauss': 4.643856189774724}}, 'Stern': {'estimate': {'time': 9.579315937580013, 'memory': 8.60733031374961, 'parameters': {'r': 0, 'p': 2, 'l': 4}}, 'additional_information': {'permutations': 0, 'gauss': 4.643856189774724, 'lists': [3.321928094887362, 2.6438561897747244]}}}


Docker
^^^^^^
Run :bash:`make docker-run` to get a shell in the freshly created docker imager. Afterwards execute :bash:`sage` to get
a sage shell:

.. code-block:: bash

    root@31d20617c222:/home/cryptographic_estimators# sage
    ┌────────────────────────────────────────────────────────────────────┐
    │ SageMath version 9.0, Release Date: 2020-01-01                     │
    │ Using Python 3.8.10. Type "help()" for help.                       │
    └────────────────────────────────────────────────────────────────────┘
    sage: from cryptographic_estimators.SDEstimator import SDEstimator
    sage:

.. note::

    If you encounter any problem please see :ref:`troubleshooting`.


Documentation
=============
If you want to deep dive in the library, check how it works and what you can do with it, you can generate
the documentation on you own or use the online `documentation <https://crypto-tii.github.io/cryptographic_estimators/>`_

To generate the documentation locally you can run ``make doc`` and then open to ``docs/build/html/index.html`` to view
it. Or you can also generated the documentation through docker via running ``make docker-doc``



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

.. _troubleshooting:
Troubleshooting
================
TODO


Examples (Please Ignore, this is just for testing)
==================================================

To check the correctness of the shown examples run:

.. code-block:: bash

    sage --python -m pytest --doctest-modules --accept docs/source/user_guide.rst


.. This is a comment.


.. note::

   This project is under active development.



Lorem ipsum [#f1]_ dolor sit amet ... [#f2]_

.. rubric:: Footnotes

.. [#f1] Text of the first footnote.
.. [#f2] Text of the second footnote.
