# Movies

Simple Django Rest Framework app providing REST API with movies downloaded from [OMDB API](http://www.omdbapi.com/).

[![Build Status](https://travis-ci.org/kubked/movies.svg?branch=master)](https://travis-ci.org/kubked/movies) [![Coverage Status](https://coveralls.io/repos/github/kubked/movies/badge.svg)](https://coveralls.io/github/kubked/movies)

## Running locally

### Prerequisites

Install PostgreSQL 9.5+, Python 3.7 and Django 2.1

Create postgres account for Movies and write it's name in `src/core/local_settings.py` [(see more)](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) or export it in environment setting `DATABASE_URL` [(see dj-database-url)](https://github.com/kennethreitz/dj-database-url). Example:
```
DATABASE_URL=postgres://moviesuser:movies@localhost:5432/movies
```

Before installation and first usage you need to request for [OMDB API](http://www.omdbapi.com/)-key and then store it in environment setting `OMDB_API_KEY`. If you don't want to store it in env you have to add it before all `manage.py` and `gunicorn` commands.

### Installing

Run requirements installation and migrations:
```
pip install -r requirements.txt
cd src
python manage.py migrate
```
or if you don't have `OMDB_API_KEY` in env:
```
OMDB_API_KEY=abcdefg python manage.py migrate
```

### Running the server
To run server locally use gunicorn:
```
gunicorn core.wsgi --log-file=- --pythonpath=src
```

## Running the tests
Running django unit tests:
```
cd src && python manage.py test
```

## API specification

See [API.md](API.md) file.

## License

Almost whole project is provided on MIT License - see the [LICENSE.md](LICENSE.md), feel free to use each part of the project you want, except API specification.

I'm not the author of API architecture and I can't grant any permission to reuse it.
