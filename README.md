# flask-url-shorter
This is a URL shortener API made with [Flask](https://flask.palletsprojects.com/en/1.0.x/).

It creates short links by generating unique hashes and associating them to long URL addresses. It also redirects short URLs requests to their full address counterparts. URL data is locally stored on a SQLite database, through [SQLAlchemy](https://www.sqlalchemy.org/).

---

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

You also have the option to erase the database or populate it with a few URLs from a static CSV file in the assets directory, with the commands below. Note that erasing the database is irreversible.

```
flask destroy-db

flask populate-db
```

---

### Usage

#### Tests

Tests were written using the [pytest](https://docs.pytest.org/) framework. To run, simply execute `pytest` on the command line with your virtual environment activated.

#### Making requests

This API listens to the following routes:

- `/shorten-url`

   Methods: `POST`

   This is the URL shortening endpoint. A JSON request body is expected, containing a single key-value pair with the URL to be shortened. Successful requests will receive a response containing the short URL. Examples of valid request and response bodies can be seen below:

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

   The long URL address is submitted to a validation process, which involves a regex that ensures a valid URL format. Either `"https://"` or `"http://"` at the beginning of the URL is also required. Invalid or missing data is met with a `400` response accompanied by an error message.

- `/lil/<hash>`

   Methods: `GET`, `DELETE`

   This is the short URL handler endpoint. GET requests are redirected to their corresponding long address counterpart, while DELETE requests removes URLs from the database. `404` responses are returned for not found URLs.  Successful GET requests will also increment a click counter that keeps track of short URL usage.

- `/lil/<hash>/clicks`

   Methods: `GET`

   This is the clicks counter endpoint. It responds with an object containing a count of how many times the short URL has been accessed through API requests. Alternatively returns a `404` if a URL with the given hash is not found. Below follows an example of a successful response:

   ```
   {
     "clicks": 17,
     "msg": "This short URL has been accessed 17 times."
   }
   ```
  
- `/get-all`

   Methods: `GET`

   This endpoint returns all data from the database as an array of objects. It is intended as a development endpoint. A response example follows:

   ```
   [
     {
       "clicks": 3,
       "long_url": "https://www.example-1.com",
       "hash": "Pmg0"
     },
     {
       "clicks": 5,
       "long_url": "https://www.example-2.com",
       "hash": "Ppe9"
     }
   ]
   ```
