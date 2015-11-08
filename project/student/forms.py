# project/student/forms.py


from flask_wtf import Form
from wtforms import SelectField

from project.models import Course


def get_courses():
    courses = Course.query.all()
    if courses:
        return courses


class AddCourseForm(Form):
    get_all_courses = get_courses()
    if get_all_courses:
        courses = SelectField(
            u"Available Courses",
            choices=[
                (single_course.name, single_course.name)
                for single_course in get_all_courses
            ]
        )
