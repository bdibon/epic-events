# epic-events

A CRM system powered by django-admin and django-rest !

Epic events is supposed to be a startup whose specialty is event planning an management, there are different teams such as the *management*, the *sales* and the *support* team that all have specific permissions on the different entities of the application.

Only salespersons can add clients and make them sign contracts, then each salespersons is responsible of its own clients/contracts portfolio.

Support consultants are responsible for updating the events they have been assigned to, and managers are all mighty.

The app has been built with django and django-rest-framework, it provides an admin interface on the `/admin` route and a RESTful API on `/api`.

## Setup

You first need to create a virtual environment for the project.

```
pipenv shell
```

Then install the required dependencies.

```
pipenv install
```

Note that in the latest commits the database engine has been configured to run with postgres, you might change it back to sqlite if you want to.

Now apply the migrations to your database.

```
py manage.py migrate
```

Finally the app should be up an running with the `py manage.py runserver` command.

You will need to create a superuser if you want to start fiddling with the admin interface or the API.

## API Documentation

You can find the online documentation of the API [here](https://documenter.getpostman.com/view/7484015/UyrBkGf7).
