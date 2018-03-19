# manage.py

import unittest
import coverage
from flask_script import Manager
from project import db, create_app
from project.api.users.user_models import User
from flask_migrate import MigrateCommand


COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*'
    ]
)
COV.start()

app = create_app()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def recreate_db():
    """ Recreates a database """
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def seed_db():
    """Seeds the database."""
    # db.create_all()
    db.session.add(User(username='peter', email="petertahinduka@gmail.com"))
    db.session.add(User(username='paulampurire',
                        email="paulampurire@gmail.org"))
    db.session.add(User(username='michael', email="michael@realpython.com"))
    db.session.add(User(username='michaelherman', email="michael@mherman.org"))
    db.session.commit()


if __name__ == '__main__':
    manager.run()
