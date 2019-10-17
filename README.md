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
  

# Development Utils

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
