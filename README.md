# Virtuosi

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ python -m venv myvenv
$ source myvenv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app.