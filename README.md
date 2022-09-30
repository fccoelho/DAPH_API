# API for the Decentralized Autonomous Publishing House (DAPH)
This project is the data backend and web frontend of the DAPH.

It is based of Django-Ninja. 

to get started in development, first make sure you have [poetry](https://python-poetry.org/) installed on your computer.

```Bash
$ poetry install
$ poetry shell
$ ./manage.py migrate
$ ./manage.py createsuperuser
$ ./manage.py runserver
```

After running the commands above, you can point you
browser [http:localhost:8000/api/docs/](http://localhost:8000/api/docs/).
