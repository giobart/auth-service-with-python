[![Build Status](https://travis-ci.org/giobart/auth-service-with-python.svg?branch=master)](https://travis-ci.org/giobart/auth-service-with-python) [![Coverage Status](https://coveralls.io/repos/github/giobart/auth-service-with-python/badge.svg?branch=master)](https://coveralls.io/github/giobart/auth-service-with-python?branch=master)

# Auth Service with Python

This is an example of how to create a service that authenticate users via JWT token as a cookie.

To test the service you can refere to the following documentation:
[https://documenter.getpostman.com/view/9458914/SW7UaVqJ](https://documenter.getpostman.com/view/9458914/SW7UaVqJ)

## Execution
In order to run the application do the following:

move to the main application folder and then run

```
python setup.py develop
```

when the setup is finished just execute the app

```
python auth/app.py
```
now the application should be up and running on 127.0.0.1:5000 as default

## Test

The test suite is under the folder auth/tests/ and there is already a configuration for tox in the main folder. 
You can also test it manually with curl, postman or whatever you prefer.

enjoy and feel free to contribute
