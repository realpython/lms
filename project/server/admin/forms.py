# project/server/admin/forms.py


from flask_wtf import Form
from wtforms import TextField, DateField, TextAreaField, SelectField, \
    PasswordField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError

from project.server.models import Course, Teacher, Student


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
    teachers = SelectField('Taught By')
    students = SelectMultipleField(
        'Add Students',
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
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
    teachers = SelectField('Taught By')
    current_students = SelectMultipleField(
        'Remove Students',
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )
    potential_students = SelectMultipleField(
        'Add Students',
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )


class AddStudentForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate_email(self, field):
        if Student.query.filter_by(email=field.data).first():
            raise ValidationError('Sorry. That email is already taken.')


class UpdateStudentForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    registered_on = DateField(
        'Registered On',
        validators=[DataRequired()]
    )


class AddTeacherForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirm password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )

    def validate_email(self, field):
        if Teacher.query.filter_by(email=field.data).first():
            raise ValidationError('Sorry. That email is already taken.')


class UpdateTeacherForm(Form):
    email = TextField(
        'Email Address',
        validators=[DataRequired(), Email(), Length(min=6, max=40)]
    )
    registered_on = DateField(
        'Registered On',
        validators=[DataRequired()]
    )
