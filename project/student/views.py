# project/student/views.py


###########
# imports #
###########

from flask import render_template, Blueprint
from flask.ext.login import login_required


##########
# config #
##########

student_blueprint = Blueprint('student', __name__,)


##########
# routes #
##########


@student_blueprint.route('/student/classes')
@login_required
def show_classes():
    return render_template(
        '/student/classes.html'
    )
