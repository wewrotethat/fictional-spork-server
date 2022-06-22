# fictional-spork-server
Repo for the server for Malaria Recognition using Deep Learning 

# Running the app
In order to run the app
- Install `pipenv`
- run `pipenv` install in the directory
- create a firebase project and update the gcloud_storage.py file with the correct info as well as the .env file
- create a mongo db instance and add the url to the .env file
- create a hahu sms account and add the required credentials to the .env file
- then run app.py using `python app.py` or `gunicorn app:app`
