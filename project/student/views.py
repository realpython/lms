# project/student/views.py


###########
# imports #
###########

from flask import render_template, Blueprint
from flask.ext.login import login_required
from flask.ext.login import current_user

from project.models import Class


##########
# config #
##########

student_blueprint = Blueprint('student', __name__,)


###########
# helpers #
###########

def get_classes(user_id):
    return Class.query.filter_by(user_id=user_id).all()


##########
# routes #
##########


@student_blueprint.route('/student/classes')
@login_required
def show_classes():
    return render_template(
        '/student/classes.html', classes=get_classes(current_user.get_id())
    )
