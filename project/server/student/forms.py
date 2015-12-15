# project/server/student/forms.py


from flask_wtf import Form
from wtforms import SelectField


class AddCourseForm(Form):
    courses = SelectField(u'Available Courses')
