# Todo

## Admin

1. Admin have full API access
  - Courses - read, update, delete
  - Students
  - Teachers

## Other

1. Add error handlers to db sessions:

    ```python
    try:
        session.add(c)
        session.commit()
        return True
    except sqlalchemy.exc.IntegrityError as err:
        return False
    ```

1. DRY all tests
1. DRY the APIs
1. Add assignments
1. Add quizes
1. Add grades
1. Rules for when students can drop/remove courses? (or can this only come from an admin?)
