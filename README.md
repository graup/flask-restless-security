This is a simple bootstrapped Flask Website + API using Flask-Restless, Flask-Security, SQLAlchemy and
JWT tokens for authentication.

Credits go to Nic for providing the basic idea:
http://stackoverflow.com/a/24258886/700283

I changed the structure quite a bit and added stubs for testing and templates.

Setup
=====

- Setup vitualenv
- Run `pip install -r requirements.txt`
- Start server using `python server.py`


**API auth**

- POST /auth {'username': '', 'password': ''}
- Returns JSON with {'token':''}  
- Then request from API using header 'Authorization: Bearer $token'

**Tests**

- Run tests using `python test.py`