# Todo

## Admin

1. Admin have full API access
  - Courses - create, read, update
  - Students - create, read, update
  - Teachers
  - Users

## Other

1. Add error handlers to db sessions (and test):

    ```python
    try:
        session.add(c)
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError as err:
        return False
    ```

1. Split Admin dashboard into seperate pages (student, courses, etc.)
1. Add courses to student form; add students to course form (for admin)
1. DRY all tests (add helpers, check db for changes)
1. DRY the APIs (one central API?, refactor into proper REST structure?)
1. Refactor blueprints into, well, "blueprints" (or components) folder
1. Format dates
1. Resend password form
1. Add assignments
1. Add quizes
1. Add grades
1. Rules for when students can drop/remove courses? (or can this only come from an admin?)
1. Add coveralls / code coverage
1. Test for different versions of Python on travis
