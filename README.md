This is a simple bootstrapped [Flask](http://flask.pocoo.org/) website + API using:

- [Flask-Restless](https://flask-restless.readthedocs.org/en/latest/) (API)
- [Flask-Security](https://pythonhosted.org/Flask-Security/) (Authentication)
- [Flask-JWT](https://pythonhosted.org/Flask-JWT/) (API authentication)
- [SQLAlchemy](http://www.sqlalchemy.org/) (ORM)

Plus stubs for

- Templates
- Testing

I got the basic idea from Nic:
http://stackoverflow.com/a/24258886/700283

Setup
=====

- Create and activate a vitualenv
- Run `pip install -r requirements.txt`
- Start server using `python server.py`

**API auth**

- POST /auth {'username': '', 'password': ''}
- Returns JSON with {'token':''}  
- Then request from API using header 'Authorization: Bearer $token'

**Tests**

- Run tests using `python test.py`