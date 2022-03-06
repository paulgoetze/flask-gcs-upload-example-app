# "Uploading files to Google Cloud Storage using a Flask API" – Example App

This is the example app for our 3-part post series on Medium:

 * [Part 1](https://medium.com/p/7a4e379911d7?source=friends_link&sk=dd460418de3d1829c056db5c069f9b6d): basic app setup, configuring testing & production filedepots (see [part-1](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-1) branch)
 * [Part 2](https://medium.com/p/6b203a0e392c?source=friends_link&sk=e7274af2488285dd51756d81de9cf671): testing and implementing the User model & file upload endpoint (see [part-2](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-2) branch)
 * [Part 3](https://medium.com/p/897c302916e7?source=friends_link&sk=e9fca9639697051be296c140932884e0): customising the upload & allowing multiple depots (see [part-3](https://github.com/paulgoetze/flask-gcs-upload-example-app/tree/part-3) branch)


## Running the App

In order to run the Flask app:

* make sure you have Python v3.10+ and [pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv) installed
* run `pipenv install` to install the dependencies
* run `pipenv shell` to activate the projects virtualenv
* copy `my_app/config/app_config.py.sample` to `my_app/config/app_config.py` and adjust the config variables to your needs
* run `FLASK_APP=my_app flask db upgrade` to init the configured database
* run `FLASK_APP=my_app flask run` to start the local server
* run `pytest` to run the test suite
