# Learning Management System

Just a basic LMS... built with brute force

[![Build Status](https://travis-ci.org/realpython/lms.svg?branch=master)](https://travis-ci.org/realpython/lms)

[![Coverage Status](https://coveralls.io/repos/realpython/lms/badge.svg?branch=master&service=github)](https://coveralls.io/github/realpython/lms?branch=master)

## Quick Start

### Basics

1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/config.py*, and then run:

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="project.server.config.ProductionConfig"
```

### Create DB

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py create_users
$ python manage.py create_data
```

### Run the Application

```sh
$ python manage.py runserver
```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```
