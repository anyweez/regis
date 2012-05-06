# REGIS
Overview

## Status
We currently do not recommend that you deploy REGIS on your own systems because 
it is not yet considered to be stable in untested environments.  We are currently
running our own deployment and it is performing well but needs a couple of key
features and bug fixes before we're going to consider it safe to deploy elsewhere.

## Core features
REGIS is a system for serving customized and personalized practice problems to students / users. 
We are currently using it in our [non-majors course](http://inst.eecs.berkeley.edu/~cs10) 
at UC Berkeley and are developing it for college, K-12 and informal learning environments.

The core features include:
* Easy-to-use user interface based on a flash card analogy.
* A simple templated question authoring language that can be used to write questions that are
customized for different students.
* "League"-based organizations, which can be used to represent classes, sections, study groups,
or any other group of users.  We have all of our students enrolled in a single league in our
course.
* Manual or automatic question evaluation.  Authorized question authors can provide solver
scripts, which can be used to generate different question permutations for different users.
Questions that cannot be automatically solved (or questions submitted from untrusted users)
can be graded using a simple peer review interface.
* Democratized question submission that allows anyone in the league to submit practice
questions.  Only instructors or other authorized individuals can submit auto-graded questions
but anyone can submit manually-graded questions.
* Event logging that records a variety of metrics to measure comprehension among individuals
and the league as a whole.

## Installation
If you would like to try to install REGIS, the following instructions should set
you on your way.  Note that we're not considering it to be a stable project yet,
and we intend to streamline the setup process in the future.

### Dependencies
The following software packages are required in order to run a REGIS deployment.
* python-2.7 or newer
* python-django
* django-social-auth [ [https://github.com/omab/django-social-auth](https://github.com/omab/django-social-auth) ]
* Some form of database that Django supports
* Web server w/ mod\_wsgi or Passenger for production deployment

### Setup
1. Install all of the software listed above.  Installation instructions should be
available on the software's home page.
2. Get a copy of the REGIS source code by running the command `git clone git@github.com:luke-segars/regis.git`.
from the directory that you want to store the code in.  Note that this is usually not in a web-accessible
directory when using mod\_wsgi or Passenger.
3. Configure the settings in the `face/settings.py` file to match your environment.  Make sure to update the
database setting, the secret key, and the admin email addresses in particular.
4. From the `face/` directory, run the command `python manage.py syncdb`.  This is a Django command that will
connect to the database specified in your `settings.py` file and create all of the tables that REGIS needs.
5. From the `face/` directory, run the command `python manage.py setup`.  This will create all of the initial
records that REGIS needs to function correctly.  You should be prompted for a name of your first league. 
6. REGIS should now be configured on your system.  To test it, run the command `python manage.py runserver`
from the same directory.  You should be able to view your REGIS deployment by visiting `http://localhost:8000`
in your favorite web browser.
7. Note that this command launches Django's web server, which is *not* designed for production-level deployments.
If you want to launch REGIS publicly, be sure to use production-quality server software like Apache and configure
it to serve your pages.
