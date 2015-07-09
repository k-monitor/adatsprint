Adatozz
=======

A project to help digitize FoI documents.

Installation
------------

The project was developped with Python 3 in mind but should (hopefully) work
with Python 2 as well.

In a virtualenv, install the requirements (`pip3 install -r requirements.txt`).

Then create the database with `python3 manage.py migrate`.

You can import PDF into the system using the `bulk_upload` management command:
`python3 manage.py bulk_upload path_to_folder` (where `path_to_folder` points
to a folder that contains PDF files).

You might also want to create a superuser (to access the admin for example):
`python3 manage.py createsuperuser`.

Running
-------

To run the site locally, simply do `python3 manage.py runserver`.
You'll also need to serve the uploaded files if you want PDFs to load.
For that, you can use the `servemedia.py` script like so:

    $ cd uploads  # settings.MEDIA_ROOT
    $ python3 ../servemedia.py 8080  # the settings assume port 8080

Workflow
--------

A two-step process was designed with these constraints:

* Each "digitized" document should be verified once
* Concurrent editing of documents should not be possible
* To minimize waste of time, two people should not be able to work on the same
  document at once

Here's a fancy ascii-chart of the workflow (actions are in boxes, states are
next to arrows):

         +----------+
         | CREATION |
         +----------+
            |
            | EMPTY
            v
          +-------+
          | CLAIM |
          +-------+
            |
            | PROCESSING
            v
    +--------------------+
    | INITIAL PROCESSING |
    +--------------------+
            |
            | PROCESSED
            v
          +-------+
          | CLAIM |
          +-------+
            |
            | VERIFIYING
            v
       +--------------+
       | VERIFICATION |
       +--------------+
            |
            | VERIFIED
            v
           +------+
           | DONE |
           +------+

Deploying
---------

Make sure you use the correct settings file when running management commands:

    DJANGO_SETTINGS_MODULE=adatozz.settings_prod python manage.py migrate

To start gunicorn:

    gunicorn -c gunicorn_confi.py adatozz.wsgi:application

To reload gunicorn (after code change for example):

    kill -HUP $(cat adatozz.pid)
