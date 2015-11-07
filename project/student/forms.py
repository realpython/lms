# project/student/forms.py


from flask_wtf import Form
from wtforms import SelectField

from project.models import Course


def get_courses():
    return Course.query.all()


class AddCourseForm(Form):
    courses = SelectField(
        u"Available Courses",
        choices=[
            (single_course.name, single_course.name)
            for single_course in get_courses()
        ]
    )
