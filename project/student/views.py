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


@student_blueprint.route('/students/')
@login_required
def student_home():
    return render_template('/student/home.html')


# @student_blueprint.route('/students/classes/')
# @login_required
# def student_classes():
#     return render_template('/students/classes.html')


# @app.route('/students/classes/join/', methods=['POST'])
# @login_required
# def student_class_join():

# @app.route('/students/class/<class_id>/')
# @login_required
# def student_class_page(class_id):
