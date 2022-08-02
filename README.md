DJANGO BUDGET
=============

### 1. Prerequisites.
Fill ___.env___ file with the pattern below.  
SECRET_KEY - Secret key that can be generated using:
> django.core.management.utils.get_random_secret_key  

DEBUG - 0 or 1 value  
DJANGO_SUPERUSER_EMAIL - ex. admin@admin.com  
DJANGO_SUPERUSER_USERNAME - ex. admin  
DJANGO_SUPERUSER_PASSWORD - password for superuser  
POSTGRES_USER - database username  
POSTGRES_PASSWORD - database password  
POSTGRES_DB - database name  

### 1. Instalation.  
> make setup
### 2. Run the project.
> make run-server
### 3. Any other actions available.
If you want to take some manual actions with this project, you should fill the ___dev_env.sh___ file with the same data as in ___.env___ file. Then activate virtual environment using this command:
> source dev_env.sh

Please, go to Makefile.

Unfortunately, the project is not finished.
Take a look at the code.