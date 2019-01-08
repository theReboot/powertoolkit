# powertoolkit

Overview
========

This project uses python/django.
We also have a gulp setup for front-end development, to compile scss to css.

Setup
=====

You need to have the following setup for development

```
Python >= 3.5 (preferrably 3.6)
Pipenv (to install, just do `pip install pipenv`)
npm (for front-end stuff)
```

Getting Started
===============

So you have cloned the repo with

`
git clone git@github.com:theReboot/powertoolkit.git
`

Install dependencies:
---------------------

setup your dependencies for the back and front-end

```
cd powertoolkit/powerkit/
pipenv install
npm install
```

Setup your database:
--------------------

Setup your database by running 

`pipenv run ./manage.py migrate`

from the `powertoolkit/powerkit/` directory

Create a user for yourself:
---------------------------

Run `pipenv run ./manage.py createsuperuser`
and enter the username and password to be used to create your super user


Run the development server:
---------------------------

1. Make sure you are in the powertoolkit/powerkit/ directory
2. Run `pipenv run ./manage.py runserver`

To run gulp from the same directory
3. Run `gulp`

This will run the django development server on localhost:8000, also gulp will watch files for changes and compile the sass to css.

Files
=====

The html files are in `powertoolkit/powerkit/templates/`

The sass files are in `powertoolkit/powerkit/devstatic/scss/`

The css files are in `powertoolkit/powerkit/devstatic/css/`


Go to the Site
--------------

Go to `http://localhost:8000` 


Content Management System
=========================

The application uses Wagtail (https://wagtail.io/) for content management.
