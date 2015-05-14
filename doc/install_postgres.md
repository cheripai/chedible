# Setting up PostgreSQL for development 
#### *A guide through hell in ten easy steps*


1. Install PostgreSQL
2. Make your user account a PostgreSQL admin

   ```sudo -u postgres createuser -s $USER```
3. Log in as the PostgreSQL user

   ```sudo -i -u postgres```
4. Initialize the database cluster. *Might be Linux only*

   ```initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'```
5. Start PostgreSQL and enable to run as a startup process. *Required. Command is Linux systemd only*

   ```systemctl enable postgresql.service``` 
6. Create the databases used for our development purposes and exit postgres

   ```createdb data.db && createdb test.db && exit```
7. Set up virtualenv

   ```cd /path/to/chedible && workon chedble && pip install -r requirements.txt```
8. Run behave to ensure that the database is working properly. 

   ``` behave ```
9. Initialize the primary database

   ```python db_create.py```
   
10. Run the server

   ```python run.py```
   
