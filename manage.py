# manage.py


import os
import unittest
import coverage
import datetime

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=['*/__init__.py', '*/config/*']
)
COV.start()

from project import app, db
from project.models import User, Class


migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    COV.stop()
    COV.save()
    print('Coverage Summary:')
    COV.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    COV.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    COV.erase()


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@manager.command
def create_users():
    """Creates sample users."""
    student = User(
        email='student@student.com',
        password='student',
        student=True,
        teacher=False,
        admin=False
    )
    db.session.add(student)
    teacher = User(
        email='teacher@teacher.com',
        password='teacher',
        student=False,
        teacher=True,
        admin=False
    )
    db.session.add(teacher)
    admin = User(
        email='ad@min.com',
        password='admin',
        student=False,
        teacher=False,
        admin=True
    )
    db.session.add(admin)
    db.session.commit()


@manager.command
def create_data():
    """Creates sample data."""
    user = User.query.filter_by(email='teacher@teacher.com').first()
    first_class = Class(
        name='Philosophy 101',
        description='From Plato to Socrates...',
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        user_id=user.id
    )
    db.session.add(first_class)
    second_class = Class(
        name='Music Appreciation',
        description='This class teaches you how to understand \
                     what you are hearing.',
        start_date=datetime.datetime.now(),
        end_date=datetime.datetime.now(),
        user_id=user.id
    )
    db.session.add(second_class)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
