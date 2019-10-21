# World Development - Database

## Requirements:
* This tutorial assumes a Ubuntu installation (specifically: 18.04)
* Assumes pipenv

## Get code and setup basics:

Create your project folder and cd into it.
Now enter:

```
> git clone https://github.com/genughaben/world-development.git
> pipenv install
> pipenv shell
```

## Create and setup config.cfg

Copy and customize config values:
```
>  cp config_template.cfg config.cfg 
```

Now, customize values in the newly created config.cfg as required.
  
NB: config.cfg is automatically excluded from git repo. If you should use another name, add it got .gitignore and update config variable usage across project.
  
# Local ETL

## Local airflow + local target PostgreSQL in docker containers

Setup:
```
> docker build --rm --build-arg AIRFLOW_DEPS="datadog,dask" -t puckel/docker-airflow .
> docker build --rm --build-arg PYTHON_DEPS="flask_oauthlib>=0.9" -t puckel/docker-airflow .
```

Start airflow locally:
```
> cd airflow/local
> docker-compose -f docker-compose-LocalExecutor.yml up
```

Now you can reach airflow in your browser entering: localhost:8080/admin.

**Sources:** Installation is based on [https://github.com/puckel/docker-airflow]

## Configure target PostgreSQL setup

* Update init.sql as you please
* Update requirements.txt as you please

## Enter PostgreSQL in docker container:

Make sure your docker-container is running
```
> docker exec -it local_db_1 bash
bash> psql -U postgres
```

## Configure airflow via UI:

Goto localhost:8080/admin
* Open Admin -> Connections
* Create new connection with clicking on "Create"
  
|Field    |Field value|
|---------|-----------|
|Conn Id  | postgres  |
|Conn Type| Postgres  |
|Host     | db        |
|Schema   | dummy     |
|Login    | postgres  |
|Password | postgres  |
|Port     | 5432      |


## DEVELOPMENT: SCRIPT BASED

Prerequisits:
* Make sure you have a local installation of PostgreSQL and its running. This means entering the following should not result in an error and open PostgreSQLs CLI:

### PANDAS BASED (very slow)

Login to postgresql CLI and create a Database called 'dummy'. 

```
> sudo -u postgres psql

# Make sure your use as CreateDB rights
psql-cli> CREATE DATABASE dummy;
```

Now you can execute:
```
# create world Database and Tables
> python local-etl/create_table.py

# execute ETL:
> python local-etl/pandas-etl.py
```

### SPARK BASED
```
> sudo -u postgres psql

# Now create a Databse if you have not done so alread:
psql-cli> CREATE DATABASE world; 
```

If you have customized your config.cfg as required you can run:
```
> python local-etl/spark-etl
```
  
to execute the spark based etl script.

### SPARK CONTAINER:
The spark container has its origin in the image of bde2020/spark-master:latest and is defined in   
docker-compose-LocalExecutor.yml
  
It uses spark_jars defined in /spark_jars  
and spark_scripts and config files in spark_scripts (mounted as volumes)  
  
Spark submit:  
```
# First enter container:
>  docker exec -it local_spark_1 bash

# Next execute spark script like so:
> /spark/bin/spark-submit --master local[*] --driver-class-path /spark_jars/postgresql-42.2.8.jar /simple-app/stage_commodities.py
```


# Development Utils

#### Install and setup Postgresql DB
```
> sudo apt-get install postgresql postgresql-contrib
```
Creating a role:
```
> sudo -u postgres psql
```

Create a Postgres user for airflow (still in psql console)

```
postgres=# CREATE USER <your-user-name> PASSWORD <your password>;
CREATE ROLE
postgres=# CREATE DATABASE <your-db-name>;
CREATE DATABASE
postgres=# GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO <your-user-name>;
GRANT
postgres=# \du
 List of roles
 Role name | Attributes | Member of
 — — — — — -+ — — — — — — — — — — — — — — — — — — — — — — — — — — — — — — + — — — — — -
 <your-user-name> | | {}
 postgres | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

Add CREATE DB rights to <your-user-name>:
```
psql> ALTER USER <your-user-name> CREATEDB; 
```

Not exit console and check whether database is setup and can be accessed by user <your-user-name>

```
> psql -d airflow
psql (10.10 (Ubuntu 10.10-0ubuntu0.18.04.1))
Type "help" for help.
airflow=> \conninfo
```

You should see something like this:
```
You are connected to database "airflow" as user "<your-user-name> " via socket in "/var/run/postgresql" at port "5432".
airflow=>
```

#### Configure pg_hba.conf and postgresql.conf

##### pg_hba.conf
In order to allow airflow access to Postgres, pg_hba.conf needs to be configured:

```
> sudo nano /etc/postgresql/10/main/pg_hba.conf
```

Change int entry 'IPv4 local connections' the ADDRESS to 0.0.0.0/0 and the METHOD to trust.
In the end there should be:
```
# IPv4 local connections:
TYPE    DATABASE    USER    ADDRESS     METHOD
...
# IPv4 local connections                            <- replace line after this with next line
host    all         all     0.0.0.0/0   trust       <- use this line as replacement
```

You now need to restart Postgres entering:

```
> sudo service postgresql restart
```

##### postgresql.conf

Open postgresql.conf entering:

```
> sudo nano /etc/postgresql/10/main/postgresql.conf
```

Update in the section 'CONNECTIONS AND AUTHENTICATION' listen_addresses from 'localhost' to '*'
```
# — Connection Settings -
#listen_addresses = ‘localhost’     # what IP address(es) to listen on;           <-- before
listen_addresses  = ‘*’             # for Airflow connection                      <-- after
```

And restart Postgres again:
```
> sudo service postgresql restart
```

Based on https://medium.com/@taufiq_ibrahim/apache-airflow-installation-on-ubuntu-ddc087482c14  
Also helpful: https://medium.com/@srivathsankr7/apache-airflow-a-practical-guide-5164ff19d18b

Using local PostgreSQL for testing purposes
Enter CLI:
```
> sudo -u postgres psql 
```
  
Helpful commands:  
    
| command | comment |
|----------|-----------------|
|\du | show user|
|\l | displays list of databases|
| \c <database_name> | choose database for usage |
|\dt | show tables |
|\d <table_name> | show table schema|





Further reading: 
* https://blog.usejournal.com/testing-in-airflow-part-1-dag-validation-tests-dag-definition-tests-and-unit-tests-2aa94970570c
