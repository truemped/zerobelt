.. _pyzmq: https://github.com/zeromq/pyzmq
.. _pyzmq-ctypes: https://github.com/svpcom/pyzmq-ctypes

Zero Belt
=========

This will be my small collection of useful stuff for ZeroMQ with Python.


Contents
========

So far I have copied the eventloop from pyzmq_ in order to be able to use the
same loop with pyzmq_ and pyzmq-ctypes_, which can be used with PyPy.

The next steps include the implementation of various patterns from the `ZeroMQ
Guide <http://zguide.zeromq.org/>`_, namely::

- Suicidal Snail Pattern
- {Lazy, Simple, Paranoid} Pirate Pattern


License
=======

Except noted otherwise the code is release under **Apache License, Version
2.0**. Parts that have been adopted from pyzmq_ are licensed unter **GNU
General Public License, Version 3.0**.
