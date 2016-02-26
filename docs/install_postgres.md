# Setting up PostgreSQL for development on Linux
#### *A guide through hell in six easy steps*


1. Install PostgreSQL
2. Make your user account a PostgreSQL admin

   ```sudo -u postgres createuser -s $USER```
3. Log in as the PostgreSQL user

   ```sudo -i -u postgres```
4. Initialize the database cluster

   ```initdb --locale en_US.UTF-8 -E UTF8 -D '/var/lib/postgres/data'```
5. Start PostgreSQL and enable to run as a startup process. *For systemd only*

   ```systemctl start postgresql.service && systemctl enable postgresql.service``` 
6. Create the databases used for our development purposes and exit postgres

   ```createdb data.db && createdb test.db && exit```
