# project/student/forms.py


from flask_wtf import Form
from wtforms import SelectField

from project.models import Class


def get_classes():
    return Class.query.all()


class AddClassForm(Form):
    classes = SelectField(
        u"Available Classes",
        choices=[
            (single_class.name, single_class.name)
            for single_class in get_classes()
        ]
    )
