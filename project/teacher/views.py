# project/teacher/views.py


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

teacher_blueprint = Blueprint('teacher', __name__,)


###########
# helpers #
###########

def get_classes(user_id):
    return Class.query.filter_by(user_id=user_id).all()


##########
# routes #
##########


@teacher_blueprint.route('/teacher/<int:user_id>/classes/')
@login_required
def classes(user_id):
    return render_template(
        '/teacher/classes.html', classes=get_classes(current_user.get_id())
    )

# @teacher_blueprint.route('/teacher/classes/<int:user_id>')
# @login_required
# def classes(user_id):
#     return render_template(
#         '/teacher/classes.html', classes=get_classes(current_user.get_id())
#     )

