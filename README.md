# "Uploading files to Google Cloud Storage using a Flask API" – Example App

This is the example app for our 3-part post series on Medium:

 * [Part 1](https://medium.com/p/7a4e379911d7): basic app setup, configuring testing & production filedepots (see [part-1](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-1) branch)
 * [Part 2](https://medium.com/p/6b203a0e392c): testing and implementing the User model & file upload endpoint (see [part-2](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-2) branch)
 * [Part 3](https://medium.com/p/897c302916e7): customising the upload & allowing multiple depots (see [part-3](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-3) branch)


## Running the App

In order to run the Flask app:

* make sure you have Python v3.7.x and pipenv installed
* run `pipenv install` to install the dependencies
* run `pipenv shell` to activate the projects virtualenv
* copy `my_app/config/app_config.py.sample` to `my_app/config/app_config.py` and adjust the config variables to your needs
* run `FLASK_APP=my_app flask db upgrade` to init the configured database
* run `FLASK_APP=my_app flask run` to start the local server
