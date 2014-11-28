BookBrat
========

A bookstore inventory system.

Get the Code
------------

I use the following file tree to hold the project:

```
~/Dev/python/                          (my python development directory)
     |
     +--> bookbrat_dj/                 (the project container directory)
               |
               +--> bookbrat/          (the project directory itself)
               +--> install-bookbrat/  (README.md + settings.py repo)
               +--> lib/               (links to virtualenv directories)
               +--> <other>/           (other misc directories)
```

Create a *project container* directory to hold the *project directory* itself. I called it `bookbrat_dj` and put it in my `$HOME/Dev/python` directory. So, for example, you might do:

    $ mkdir -p ~/Dev/python/bookbrat_dj
    $ cd ~/Dev/python/bookbrat_dj

Now you can clone the code into the project container directory. **If you already have `git` installed then ignore the first step below.**

    $ sudo apt-get update && sudo apt-get install git
    $ git clone http://joseph8th.com/privgit/bookbrat.git

You will be prompted for the username and password I provided, and `git` will clone the repository into a new `bookbrat` directory.

Finally, enter the `bookbrat` project, checkout the `dev` branch, and create your own development branch off of `dev`. Like this:

    $ cd bookbrat
    $ git checkout dev
    $ git checkout -b ken

Preliminary Setup
-----------------

Installing Python web apps requires some preliminary setup. We're going to do the following:

* Create a Python virtual environment -- a `virtualenv` -- for the app.
* Download and install the app's dependencies using `pip`.

### Create a Virtualenv

Create a Python-2.7 `virtualenv` for the project. I prefer to use `pyenv` with the `pyenv-virtualenv` plugin. To install both, try the [pyenv installer](https://github.com/yyuu/pyenv-installer) using the following command:

    $ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash

First use `pyenv` to install Python 2.7.6:

    $ pyenv install 2.7.6

Now create a `virtualenv` named `bookbrat`:

    $ pyenv virtualenv 2.7.6 bookbrat

Next enter the `bookbrat` project directory and set the Python version to use this `virtualenv`:

    $ cd bookbrat
    $ pyenv local bookbrat

This will create a hidden `.python-version` file in your project directory. To test it out try the following:

    $ python --version    ## should be 'Python 2.7.6'
    $ pip freeze          ## should be only 'wsgiref==0.1.2' or similar

### Install Dependencies

See the [pip](http://pip.readthedocs.org/en/latest/user_guide.html#requirements-files) `REQUIREMENTS` file for a list of Python dependencies. To install them, just do:

    $ pip install -r REQUIREMENTS

You'll see lots of warnings, but at the end it should say, "Successfully installed ..." Now the output of `pip freeze` should be identical to the `REQUIREMENTS` file.

Setup Your Environment
----------------------

Now we setup your machine to serve the web app locally. This involves:

* Move the `settings.py` file into the `bookbrat` project directory.
* Creating a local Apache2 virtual server to serve static files -- CSS, images, JavaScript, etc.
* Creating a local SQLite3 database file.

### Move settings.py

To make development easier, I've separated the `settings.py` file from the web app itself. In production, we'd use our web host's server (Apache) and database (PostgreSQL).

You'll find `settings.py` in this repository. Just clone it from GitHub into your *project container* directory (i.e., `bookbrat_dj`). If you're in the `bookbrat` directory, just do:

    $ cd ..
    $ git clone https://github.com/install-bookbrat

Now just copy it into the `bookbrat/bookbrat` directory:

    $ cp install-bookbrat/settings.py bookbrat/bookbrat

### Create Static App
