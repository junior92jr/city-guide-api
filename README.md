# Location Advisor Backend

This backend project is a Rest Api that provides touristic information for a Frontend project.
Main source of the information comes from OpenStreetMap through the Overpass API:

* https://www.openstreetmap.org/
* https://overpass-api.de/

It provides places for touristic destinations based on your current location.

This API should provide dynamic information that will be displayed in a frontend project.

## Usage

This project stills on development but already provides functional endpoints ready to use:

### How to Authenticate
Auth endpoint:
```
(POST) /api/v1/api-token-auth/
```
Body Request:
```
{
  "username": "user",
  "password": "user_pass"
}
```
Response:
```
{
    "token": "fbfd14c374618e78bc9bbe1f6a576489a94f61f7"
}
```

### How to use the location service

Get all recomendations from your current location:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587
```

Get all the categories available from current results.

```
(GET) /api/v1/categories/?lat=50.1101038&lng=8.6771586
```

Get all places on a radius range in meters:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587&search_radious=62
```

Get all places filterd by category:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587&category=12334
```

where "12334" is the generated category ID returned by the categories endpoint.


## Configure the project

This project uses [uv](https://docs.astral.sh/uv/) for Python dependency and virtual environment management.

### Clone the project

First verify your SSH Keys on github configuration
then if you dont have a key that points to your computer follow this tutorial:

* https://docs.github.com/de/developers/overview/managing-deploy-keys

```
$ git clone git@github.com:junior92jr/location-advisor-backend.git
```

### Install dependencies

From the project root, sync the environment:

```bash
uv sync
```

### Setting up environment variables

Create a `.env` file in the project root, next to `manage.py`.

Required variables:

```env
SECRET_KEY=django-insecure-local-dev-change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
DATABASE_URL=sqlite:///db.sqlite3
CACHE_LOCATION=.cache
OPEN_STREET_MAP_OVERPASS_URL=https://overpass-api.de/api/interpreter
OPEN_STREET_MAP_USER_AGENT=city-guide-api-demo
```

Use a real `SECRET_KEY` outside local development.

Supported `DATABASE_URL` examples:

```env
DATABASE_URL=sqlite:///db.sqlite3
DATABASE_URL=postgres://user:password@localhost:5432/city_guide
```

# Running the project
## Run the project

Once you have everything ok, you can run the project.

```bash
uv run python manage.py check

uv run python manage.py migrate

uv run python manage.py runserver
```

## Run tests

Coverage is configured for the project for running tests and measuring in Scrutinizer

```bash
uv run coverage run --source="." manage.py test --verbosity=2
```

Once ran, if you want to see fast the results you can run

```bash
uv run coverage report
```

or you can run 

```bash
uv run coverage html
```

and an HTML view of your test coverage will be generated in htmlcov/index.html

Note: Coverage stills missing but tests are running with test.py django command.

# Build Documentation

Sphinx is configured to build a user friendly site for code documentation.

To build this files run

```
(city_guide) $ cd docs
(city_guide) $ make html
```

They will be build in docs/build/html/ with index.html as the main page.
It can also be accessed from the admin site in the top navigation.

Note: Docstrings ready for Documentation but adding the library is missing.
