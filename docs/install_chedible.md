# Setting up chedible on your machine

#### Prerequisites
1. Python 3 
1. [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 
3. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) (*recommended*)
4. [PostgreSQL](https://github.com/CheriPai/chedible/blob/master/docs/install_postgres.md)
5. ```mkvirtualenv chedible```

#### Commands to run frequently (*after each update*)
1. ```cd /path/to/chedible```
1. ```workon chedible```
1. ```git pull origin master```
1. ```pip install -r requirements.txt```

**The following three commands should only be run if the schema was updated:**

1. ```dropdb data.db && dropdb test.db``` (*As a PostgreSQL admin & if these databases already exist*)
1. ```createdb data.db && createdb test.db```
1. ```python db_create.py```

#### Starting the server
1. ```python run.py```
2. Visit ```localhost:5000``` in your web browser

#### Testing the server
1. ```behave```
