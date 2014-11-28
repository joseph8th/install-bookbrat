BookBrat
========

A bookstore inventory system.

Get the Code
------------

I use the following file tree to hold the project. Substitute your python dev directory for `~/Dev/python` wherever you see it in this document.

```
~/Dev/python/                (my python development directory)
|
+--> bookbrat_dj/            (the project container directory)
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

**NOTE**: testing this I noticed that a couple dependencies did not install correctly this way: `django-debug-toolbar` and `sqlparse`. If you have anything missing, just install them individually, like so:

    $ pip install django-debug-toolbar sqlparse

Finally, let's symlink the `virtualenv` you created earlier into your project *container* directory. (Otherwise you might forget where it is!)

    $ cd ~/Dev/python/bookbrat_dj
    $ ln -s ~/.pyenv/versions/bookbrat/* .

You will now see `bin`, `include` and `lib` directories in `bookbrat_dj`.

Setup Your Environment
----------------------

Now we setup your machine to serve the web app locally. This involves:

* Move the `settings.py` file into the `bookbrat` project directory.
* Creating a local Apache2 virtual server to serve static files -- CSS, images, JavaScript, etc.
* Creating a local SQLite3 database file.

### Move settings.py

To make development easier, I've separated the `settings.py` file from the web app itself. In production, we'd use our web host's server (Apache) and database (PostgreSQL).

You'll find `settings.py` in this repository. Just clone it from GitHub into your *project container* directory (i.e., `bookbrat_dj`):

    $ cd ~/Dev/python/bookbrat_dj
    $ git clone https://github.com/joseph8th/install-bookbrat.git

Now just copy `settings.py` into the `bookbrat/bookbrat` directory:

    $ cp install-bookbrat/settings.py bookbrat/bookbrat

### Create Static App

For security reasons, Django is designed to use a separate static app. This will involve a few steps:

* Install and configure Apache2 web server.
* Create a VirtualServer for our static and media files.

#### Install and Configure Apache2

If you don't already have [Apache2](https://httpd.apache.org/) on your dev box, then the easiest way to get it going is to use `tasksel`. Like this:

    $ sudo apt-get install tasksel
    $ sudo tasksel install lamp-server

(At one point `tasksel` will prompt you for a MySQL root password. I usually use the same password as my system, but YMMV.)

Apache2 should now be running. To test this, open your browser to `http://localhost`. It should say, "It Works!". See [this tutorial](http://www.maketecheasier.com/install-and-configure-apache-in-ubuntu/) for some more info.

Now we'll tweak the Apache2 configuration a bit. Open the `apache2.conf` file as a superuser using your favorite text editor (I use [emacs](https://www.gnu.org/software/emacs/) but [nano](http://nano-editor.org/) is easier to learn and pre-installed in Ubuntu):

    $ sudo $EDITOR /etc/apache2/apache2.conf

Scroll down to the "Global Configuration" section and look for `# ServerName: localhost`. If you find it, just uncomment it (delete the '# '). Otherwise, type it in (no '#') at the top of the section and save the file.

Now we're going to take ownership of the www document root, `/var/www`. We'd **never** do this on a production server, but for development it's going to save a lot of `sudo`-ing and permissions issues.

Open `/etc/apache2/envvars` as superuser in your editor and find where it says:

``` bash
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
```

Change both of the `www-data` to *your username*, i.e., whatever you get when you do:

    $ echo $USER

Save and exit. Now let's take ownership of the www doc root, and restart Apache2:

    $ cd /var
    $ sudo chown -R $USER:$USER www
    $ sudo service restart apache2

If all went well, you should still be able to browse to `http://localhost` and you will no longer get a warning about having an unset `ServerName`.

#### Create a VirtualServer

Now we need to create a `VirtualServer` for our static app. I've included the `bookbrat.conf` file in this repository, so we'll just copy it into the `/etc/apache2/site-available` directory, like so:

    $ sudo cp ~/Dev/python/bookbrat_dj/install-bookbrat/bookbrat.conf /etc/apache2/sites-available

If you read `bookbrat.conf`, you'll see a line that reads, `DocumentRoot "/var/www/bookbrat"`. We need to create this directory and create symbolic links to our app's `static` and `media` directories in it. Like so:

    $ mkdir /var/www/bookbrat    ## don't need 'sudo' anymore!
    $ cd /var/www/bookbrat
    $ ln -s ~/Dev/python/bookbrat_dj/bookbrat/bookbrat/static .
    $ ln -s ~/Dev/python/bookbrat_dj/bookbrat/bookbrat/media .

Next we need to enable the VirtualServer so that Apache2 can directly access the app's static files (again, we'd never do this in production):

    $ sudo a2ensite bookbrat

Restart Apache2 again (`sudo service apache2 restart`) and browse to `http://bookbrat.local`. You should now see "Index of /" and our static files. Now when the web app is running it can load the CSS and any other goodies we throw in there! Wheeee!

### Create Local Database

Now all we need to do is pull everything together and create a local database file named `sqlite3.db` as defined in `settings.py`. Just change back to the project directory `bookbrat` and use Django's `manage.py` util:

    $ cd ~/Dev/python/bookbrat_dj/bookbrat
    $ python manage.py syncdb

Django will create the `sqlite3.db` DB file and schema based on what's defined in each app's `models.py` file. The first time you run it, it will ask you to create a superuser.

That's it! Your database is ready to be populated with data.

You're Almost There!
--------------------

All the boring setup work is almost over. Any minute now you can start hacking on the project. Next we're going to collect the static files and run the Django development server to make sure everything is working right:

    $ python manage.py collectstatic    ## say 'yes' to collect
    $ python manage.py runserver

This last command will fire up the dev server and give you an address where you can view the `bookbrat` on your machine. Any changes you make to the project's files will be reflected on reload in your browser.

### Seeing Your Changes

When you change the *fields* in any `models.py` file, you will need to drop that table from the DB and run `syncdb` again to regenerate the table. Changes to other parts of a model will be available on refresh.

For example, in the `Book` model, if you change this:

``` python
    author_ids = models.CharField(max_length=200, blank=True, null=True)
```

To this:

``` python
    author_ids = models.CharField(max_length=200)
```

Then you will have to drop the `packages_book` table and run `syncdb` again to see your changes (which would be to make `author_ids` a required, non-null field).

But if you changed this:

``` python
    def save(self, *args, **kwargs):
        self.date_added = datetime.now()
        if not self.myprice:
            self.myprice = 0.0
```

To this:

``` python
    def save(self, *args, **kwargs):
        self.date_added = datetime.now()
        if not self.myprice:
            self.myprice = 200.0
```

Then the change would be there on refresh in your browser (which would set the price of a book to $200.00 if the `price` form field was left empty on save).

Recommended Docs and Tools
--------------------------

Now that you have `bookbrat` up and running on your dev machine, you're gonna wanna hit the books. You'll also want some dev tools to play with.

### Dev Tools

**Web Browser:** [Firefox Developer Edition](https://www.mozilla.org/en-US/firefox/developer/) with [Firebug Add-on](https://addons.mozilla.org/en-US/firefox/addon/firebug/) - indispensable for HTML5, CSS and JavaScript coding. Let's you shape the front-end like clay, then just copy the changes into the code-base.

**SQLite3 DB Manager:** [sqliteman](http://sqliteman.yarpen.cz/) - just `apt-get install` it, point it at your `sqlite3.db` file, and go. You'll need this for dropping tables before running `syncdb`.

**Integrated Development Environment:** I was forced to learn `emacs` in college, but there's a steep learning curve. At work I use [Aptana Studio 3](http://www.aptana.com/) for PHP and JavaScript, but it has support for Python as well (just point it at your `bookbrat_dj/bin/python2.7` executable).

**GitHub:** [Git](http://www.git-scm.com/) version control is vital, especially when working with others. [GitHub](https://guides.github.com/introduction/flow/index.html) has great tips on workflow that every developer needs to know.

### Documentation

**Python Docs:** Python has [great docs here](https://docs.python.org/2/). We're using Version 2.7.6 but the latest Python2 docs are valid.

**Django Docs:** Django has [great docs here](https://docs.djangoproject.com/en/1.6/). We're using Version 1.6. Also, when I was just starting with Django, [The Django Book](http://www.djangobook.com/en/2.0/index.html) was more helpful than the docs. Funnily enough the example project they use is... a bookstore.

**Stack Overflow:** And of course, search for answers and tutorials and how-tos on teh webz. 99% of the time you'll end up on [Stack Overflow](http://stackoverflow.com/).

**W3Schools Tutorials:** A great resource for HTML5, CSS, JavaScript, SQL, PHP and jQuery. [Click here and browse away](http://www.w3schools.com/). They also have quizzes that were great when I was taking assessments at interviews once a week.

### Me

Last but not least, just hit me up with any questions and I'll be happy to help. :)