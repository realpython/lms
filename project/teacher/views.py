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


##########
# routes #
##########


@teacher_blueprint.route('/teachers/')
@login_required
def teacher_home():
    classes = Class.query.filter_by(user_id=current_user.get_id()).all()
    return render_template('/teacher/home.html', classes=classes)
