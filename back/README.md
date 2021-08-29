# Setup back

You will need to run a local redis

    docker run -p 6379:6379 --restart always -d redis:latest --requirepass <REDIS_METRIC_PASSWORD>

**Replace `<REDIS_METRIC_PASSWORD>` by the one in the `.env` file**

Then add `redis` to the `/etc/hosts` file

    127.0.0.1       localhost
    127.0.0.1       redis


## Pipenv

**Note**: You will need python 3.8

Into an Ubuntu 20.04.2

    sudo apt install virtualenv python3.8-dev python3-pip python3-tk cmake


### Setup

**To install pipenv you can use pip command**

    pip install pipenv

Or

    sudo apt install pipenv

Here more information **[Pipenv](https://pipenv-fork.readthedocs.io/en/latest/index.html#install-pipenv-today)**

Pycharm support Pipenv here the [documentation](https://www.jetbrains.com/help/pycharm/pipenv.html)

**Install from Pipfile, if there is one:**

    $ cd back && pipenv install

**To install dev packages**

    $ pipenv install --dev

**To add a new package:**

    $ pipenv install <package>

**To add a new dev package**

    $ pipenv install --dev <package>

**Next, activate the Pipenv shell:**

    $ pipenv shell
    $ python --version

## Specify versions of python

Use Python 3:

    $ pipenv --python 3

Use Python3.6:

    $ pipenv --python 3.6

Use Python 2.7.14:

    $ pipenv --python 2.7.14
