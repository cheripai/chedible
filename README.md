#chedible

#### Requirements
1. Python 3 
1. [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 
3. [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) (*recommended*)
4. [PostgreSQL](https://github.com/CheriPai/chedible/blob/master/docs/install_postgres.md)


#### Setup
1. ```mkvirtualenv --python=path/to/python3 chedible```
1. ```pip install -r requirements.txt```
1. ```createdb data.db && createdb test.db```
1. ```python db_create.py```


#### To run
1. ```python run.py```


#### To test
1. ```behave```
