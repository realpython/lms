# Learning Management System

Just a basic LMS... built with brute force

[![Build Status](https://travis-ci.org/realpython/lms.svg?branch=master)](https://travis-ci.org/realpython/lms)

## Quick Start

### Basics

1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *project/config.py*, and then run:

```sh
$ export APP_SETTINGS="project.server.config.DevelopmentConfig"
```

set APP_SETTINGS="\project\server\config\DevelopmentConfig"

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

### Business Rules

#### Admin

1. Teachers and students can only be added to a course from the add/edit course forms.

#### Courses

1. Students can add themselves to a course, but they cannot remove themselves.

#### Teachers

1. Teachers can create new courses, but they cannot add students.
