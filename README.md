# Location Advisor Backend

This backend project is a Rest Api that provides touristic information for a Frontend project.
Main source of the information comes from Foursquare:

* https://foursquare.com/

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

Get all the categories available categories from current results, Foursquate offers same functionality but every time we use the endpoint it consumes our montly budget. So are handling the functionality in our side.

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

where "12334" is the ID in Foursquare for a category.


## Configure the project
### Create a virtualenv

```
$ python3 -m venv city_guide
```

This command will create a new folder with the name `city_guide`

### Clone the project

First verify your SSH Keys on github configuration
then if you dont have a key that points to your computer follow this tutorial:

* https://docs.github.com/de/developers/overview/managing-deploy-keys

```
$ git clone git@github.com:junior92jr/location-advisor-backend.git
```

### Activate your enviroment
Inside the `city_guide` folder run the following command

```
$ source bin/activate
```

After this you will see the virtualenv name in your prompt. i.e.:

```
(city_guide) $
```

### Install requirements
```
(city_guide)$ cd city_guide_backend

(city_guide)$ pip install -r requirements.txt
```

### Setting up environment variables for project

For environment variables configuration, you will need a .env file in the parent directory of the current folder.

```
(city_guide) $ touch ../.env
```

../.env example

```
DEBUG=True

SECRET_KEY="secret_key_for_django_application"

FOURSQUARE_API_KEY="external_service_api_key"
```


# Running the project
## Run the project

Once you have everything ok, you can run the project.

```
(city_guide) $ ./manage.py check

(city_guide) $ ./manage.py migrate

(city_guide) $ ./manage.py runserver
```

## Run tests

Coverage is configured for the project for running tests and measuring in Scrutinizer

```
(city_guide) $ coverage run --source="." manage.py test --settings=city_guide.test_settings --verbosity=2
```

Once ran, if you want to see fast the results you can run

```
(city_guide) $ coverage report
```

or you can run 

```
(city_guide) $ coverage html
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
