#chedible

#### Requirements
- Python 3 
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) 
- [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) (*recommended*)
- [PostgreSQL](https://github.com/CheriPai/chedible/blob/master/docs/install_postgres.md)


#### Setup
- ```mkvirtualenv --python=path/to/python3 chedible```
- ```pip install -r requirements.txt```
- ```createdb data.db && createdb test.db```
- ```python db_create.py```


#### To run
- ```python run.py```


#### To test
- ```behave```
