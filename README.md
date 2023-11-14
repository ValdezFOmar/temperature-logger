# Temperature Logger

Django backend for managing temperature readings from a microcontroler (Raspberry Pi Pico W).

> Python `v3.11.5`


# Run server

```sh
python manage.py runserver
```


# Database setup

Install mariadb and create a database like this:

```sql
CREATE DATABASE dbname CHARACTER SET utf8;
```

Then create a user and grant all permission on this database:

```sql
GRANT ALL PRIVILEGES ON dbname.* TO 'user'@'localhost';
```

Finally, add the appropriate credential to `src/.env`, migrate and create a superuser:

```sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
