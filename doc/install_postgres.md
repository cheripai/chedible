# Setting up PostgreSQL for development 
#### A step-by-step guide through hell
###### By Dat Do


1. Install PostgreSQL
2. Make your user account a PostgreSQL admin

   ```sudo -u postgresl createuser -s $USER```
3. Log in as the PostgreSQL user

   ```sudo -i -u postgres```
4. Initialize the database cluster. *Might be Linux only*

   ```initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'```
5. Start PostgreSQL and enable to run as a startup process. *Required. Command is Linux systemd only*

   ```systemctl enable postgresql.service``` 
6. Create the databases used for our development purposes

   ```createdb data.db && createdb test.db```
7. Run behave to ensure that the database is working properly

   ```cd /path/to/chedible && workon chedble && behave```
   
