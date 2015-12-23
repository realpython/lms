# project/server/teacher/forms.py


from flask_wtf import Form
from wtforms import TextField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

from project.server.models import Course


class AddCourseForm(Form):
    name = TextField(
        'Course Name',
        validators=[DataRequired(), Length(min=3, max=40)])
    description = TextAreaField(
        'Course Description',
        validators=[DataRequired()]
    )
    subject = TextField(
        'Subject',
        validators=[DataRequired()]
    )
    start_date = DateField(
        'Start Date',
        validators=[DataRequired()]
    )
    end_date = DateField(
        'End Date',
        validators=[DataRequired()]
    )

    def validate_name(self, field):
        if Course.query.filter_by(name=field.data).first():
            raise ValidationError('Sorry. That course name is already taken.')


class UpdateCourseForm(Form):
    name = TextField(
        'Course Name',
        validators=[DataRequired(), Length(min=3, max=40)])
    description = TextAreaField(
        'Course Description',
        validators=[DataRequired()]
    )
    subject = TextField(
        'Subject',
        validators=[DataRequired()]
    )
    start_date = DateField(
        'Start Date',
        validators=[DataRequired()]
    )
    end_date = DateField(
        'End Date',
        validators=[DataRequired()]
    )
