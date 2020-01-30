===========
Derex Ecommerce
===========


.. image:: https://dev.azure.com/abstract-technology/derex.ecommerce/_apis/build/status/Abstract-Tech.derex.ecommerce?branchName=master
    :target: https://dev.azure.com/abstract-technology/derex.ecommerce/_build


Derex Plugin to integrate Open edX Ecommerce


Setup
-----

* Install this package inside a derex project environment
* Add to the project derex.config.yaml ::


    plugins:
      derex.ecommerce: {}


* Add to the project Django settings ::

    TODO

Development
-----------

* Install direnv_
* Allow direnv to create the virtualenv ::

    direnv allow

* Install with pip ::

    pip install -r requirements.txt
    pre-commit install --install-hooks


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _direnv: https://direnv.net/docs/installation.html
