# Location Advisor Backend

This backend project is a REST API that provides touristic information for a frontend project.
Main source of the information comes from OpenStreetMap through the Overpass API:

* https://www.openstreetmap.org/
* https://overpass-api.de/

It provides places for touristic destinations based on your current location.

This API should provide dynamic information that will be displayed in a frontend project.

## Usage

This project is still in development but already provides functional endpoints ready to use:

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

Get places near a location:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587
```

The default search radius is `1000` meters.

Get places within a custom radius in meters:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587&search_radious=250
```

Get known categories available for filtering:
```
(GET) /api/v1/categories/
```

Filter places by a known category slug:
```
(GET) /api/v1/places/?lat=50.1101038&lng=8.6771587&category=parking
```

Example category response:
```json
{
  "categories": [
    {
      "slug": "parking",
      "name": "Parking"
    }
  ]
}
```

Example places response:
```json
{
  "places": [
    {
      "osm_id": 331124761,
      "osm_type": "node",
      "name": "Heiliger Ludgerus",
      "latitude": 51.9322712,
      "longitude": 6.9442418,
      "category": "wayside-shrine",
      "category_name": "Wayside Shrine",
      "osm_uid": "osm-node-331124761"
    }
  ]
}
```


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
CACHE_TIMEOUT_IN_SECS=86400
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

Tests are written with pytest.

```bash
uv run pytest
```

Run only the places tests:

```bash
uv run pytest places/tests
```

Run Django's system check:

```bash
uv run python manage.py check
```

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
