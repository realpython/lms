# Todo

## Testing/Errors

1. Add error handlers to db sessions (and test):

    ```python
    try:
        session.add(c)
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError as err:
        return False
    ```

1. DRY all tests (add helpers)
1. Update the tests to ensure that the db is updated (more integration tests!)
1. Add coveralls / code coverage
1. Test for different versions of Python on travis

## Admin

1. Add courses to add and edit teacher forms

## Structure

1. DRY the APIs (one central API?, refactor into proper REST structure?)

## Other

1. Add assignments
1. Add quizes
1. Add grades
1. Add courses to student form
1. Add students to add and edit course forms (for teachers)
1. Rules for when students can drop/remove courses? (or can this only come from an admin?)

## Forms

1. Update the update course form so that the course name is only checked for duplicates if it is updated in the form
