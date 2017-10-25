===============================
Edenlab
===============================

Implementation of Edenlab test task 


Quickstart
----------

First, set your app's secret key as an environment variable. For example,
add the following to ``.bashrc`` or ``.bash_profile``.

.. code-block:: bash

    export edenlab_SECRET='something-really-secret'

Run the following commands to bootstrap your environment ::

    git clone https://github.com/snowory/python-task
    cd edenlab
    pip install -r requirements/dev.txt

You will see a pretty welcome screen.

In general, before running shell commands, set the ``FLASK_APP`` and
``FLASK_DEBUG`` environment variables ::

    export FLASK_APP=autoapp.py
    export FLASK_DEBUG=1

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    flask db init
    flask db migrate
    flask db upgrade


Import GitHub repositories
--------------------------

To import GitHub open repositories, run ::

    flask import_data

This command will by default:
 - import repositories that have been written in Python and have ``rest`` keyword.
 - import just a few fields from GitHub Search API: ``full_name``, ``html_url``,
``description``, ``stargazers_count``, ``language``.


Deployment
----------

To deploy::

    export FLASK_DEBUG=0
    flask run       # start the flask server

In your production environment, make sure the ``FLASK_DEBUG`` environment
variable is unset or is set to ``0``, so that ``ProdConfig`` is used.


Shell
-----

To open the interactive shell, run ::

    flask shell

By default, you will have access to the flask ``app``.


Running Tests
-------------

To run all tests, run ::

    flask test


Migrations
----------

Whenever a database migration needs to be made. Run the following commands ::

    flask db migrate

This will generate a new migration script. Then run ::

    flask db upgrade

To apply the migration.

For a full migration command reference, run ``flask db --help``.

