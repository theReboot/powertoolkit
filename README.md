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
Now, setup your dependencies for the back and front-end

```
cd powertoolkit/powerkit/
pipenv install
npm install
```

To run the development server, you need 2 steps:

1. Make sure you are in the powertoolkit/powerkit/ directory
2. Run `pipenv shell`
3. Run `gulp`

This will run the django runserver command and open the home page on a browser, then watch files for changes and reload the browser.

Files
=====

The html files are in `powertoolkit/powerkit/templates/`
The sass files are in `powertoolkit/powerkit/devstatic/scss/`
The css files are in `powertoolkit/powerkit/devstatic/css/`
