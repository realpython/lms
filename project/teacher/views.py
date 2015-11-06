# project/teacher/views.py


###########
# imports #
###########

from flask import render_template, Blueprint
from flask.ext.login import login_required


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
    return render_template('/teacher/home.html')
