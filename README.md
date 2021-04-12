# flask-url-shorter
This is a URL shortener API made with [Flask](https://flask.palletsprojects.com/en/1.0.x/).

It creates short links by generating unique hashes and associating them to long URL addresses. It also redirects short URLs requests to their full address counterparts. URL data is locally stored on a SQLite database, through [SQLAlchemy](https://www.sqlalchemy.org/).

### Application setup

Generate virtual environment:

```
python -m venv env
source env/bin/activate
```

Install requirements:

```
python -m pip install -r requirements.txt
```

Database setup:

```
flask setup-db
```

Set and run flask app:

```
export FLASK_APP=main.py
export FLASK_ENV=development
flask run
```

You're all set.

You also have the option to erase the database and populate it with a few URLs from a static CSV file in the assets directory, with the commands below. Note that erasing the database is irreversible.

```
flask destroy-db

flask populate-db
```

### Usage

This API listens to the following routes:

- `/shorten-url`

   Methods: `POST`

   This is the URL shortening endpoint. It expects a JSON request body containing a single key-value pair with the URL to be shortened, and responds with a similar object containing the short URL:

   ```
   // Expected request body:
   {
     "url": "https://www.example.com"
   }
   
   // Response example:
   {
     "short_url": "http:/localhost:port/lil/a123"
   }
   ```

   A URL validation process takes place, requiring the passed URL to match a regex that ensures its default format. It also requires the URL to begin with either `"https://"` or `"http://"`. Missing or invalid data will cause this endpoint to respond with status code `400` and an error message.

- `/lil/<hash>`

   Methods: `GET`, `DELETE`

   This is short URL handling endpoint. It redirects GET requests to their corresponding long address counterpart, and deletes matching URL entries in DELETE requests. Should a requested short URL not be found, it returns a `404` response. Short URLs also have a clicks counter that is incremented with each request.

- `/lil/<hash>/clicks`

   Methods: `GET`

   This is the clicks counter endpoint. It simply returns a response object containing the counter for how many times the corresponding short URL has been accessed through API requests.
  
- `/get-all`

   Methods: `GET`

   This endpoint returns all data from the database. It is intended as a development endpoint.
