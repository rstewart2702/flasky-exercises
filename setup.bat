rem it's crucial to activate the virtual environment:
Scripts\activate

pip install flask
pip install flask-bootstrap

rem At end of chapter 3, we add in flask-moment:
pip install flask-moment

rem At start of chapter 4, we add in flask-wtf, for help with
rem forms handling:
pip install flask-wtf

rem At start of Chapter 5:
rem add in flask-sqlalchemy, in order to interface with databases:
pip install flask-sqlalchemy

rem Midway-through Chapter 5:
rem installation of the flask-migrate package, to ease
rem migration/maintenance of relational database changes.
pip install flask-migrate

rem Start of Chapter 6:
rem installation of the flask-mail package, to help with email management...
pip install flask-mail

rem Start of Chapter 8:
rem For the material in chapter 8, package werkzeug is also needed, but it 
rem was brought in earlier since packages installed earlier depended on it,
rem so it should be installed already.
rem 
rem Authentication-related packages:
pip install flask-login
