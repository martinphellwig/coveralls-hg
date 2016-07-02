.. image:: https://img.shields.io/codeship/5f0d5a50-2194-0134-4a97-1eef50e7a565/default.svg
   :target: https://bitbucket.org/hellwig/coveralls-hg
.. image:: https://coveralls.io/repos/bitbucket/hellwig/coveralls-hg/badge.svg?branch=default 
   :target: https://coveralls.io/bitbucket/hellwig/coveralls-hg?branch=default
.. image:: https://img.shields.io/pypi/v/coveralls-hg.svg
   :target: https://pypi.python.org/pypi/Coveralls-HG/
.. image:: https://img.shields.io/badge/Donate-PayPal-blue.svg
   :target: https://paypal.me/MartinHellwig
.. image:: https://img.shields.io/badge/Donate-Patreon-orange.svg
   :target: https://www.patreon.com/hellwig
   
############
Coveralls HG
############

What is it?
===========
- An api library to coveralls.io

What problem does it solve?
===========================
Other coveralls library require git, this one is more dvcs agnostic, but
targeted towards bitbucket. The coverage information should be a python coverage
file.

How do I install it?
====================
::

  $ pip install coveralls-hg


How do I use it?
================
::

  # The user, repo are the bitbucket variables
  # The token is the coveralls project token
  >>> from coveralls_hg.api import API
  >>> api = API(user, repo, token)
  >>> api.set_source_files(path_to_coverage_data)
  >>> api.upload_coverage()

The api has several other things that can be set additionally to upload to
coveralls.io .


What license is this?
=====================
Two-clause BSD


How can I get support?
======================
Please use the repo's bug tracker to leave behind any questions, feedback,
suggestions and comments. I will handle them depending on my time and what looks
interesting. If you require guaranteed support please contact me via
e-mail so we can discuss appropriate compensation.


Signing Off
===========
Is my work helpful or valuable to you? You can repay me by donating via:

https://paypal.me/MartinHellwig

.. image:: https://img.shields.io/badge/PayPal-MartinHellwig-blue.svg
  :target: https://paypal.me/MartinHellwig
  :alt: Donate via PayPal.Me
  :scale: 120 %

-or-

https://www.patreon.com/hellwig

.. image:: https://img.shields.io/badge/Patreon-hellwig-orange.svg
  :target: https://www.patreon.com/hellwig
  :alt: Donate via Patreon
  :scale: 120 %


Thank you!