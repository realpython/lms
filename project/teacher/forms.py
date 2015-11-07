# project/teacher/forms.py


from flask_wtf import Form
from wtforms import TextField, DateField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddClassForm(Form):
    name = TextField(
        'Class Name',
        validators=[DataRequired(), Length(min=3, max=40)])
    description = TextAreaField(
        'Class Description',
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
