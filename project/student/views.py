# project/student/views.py


###########
# imports #
###########

from flask import render_template, Blueprint, request, flash, redirect
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Class
from project.student.forms import AddClassForm


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


@student_blueprint.route(
    '/student/add_class',
    methods=['GET', 'POST']
)
@login_required
def add_class():
    form = AddClassForm(request.form)
    if form.validate_on_submit():
        print('Something needs to happen here!')
        flash('Thank you for adding a new class.', 'success')
        return redirect('/student/classes')
    return render_template('/student/add.html', form=form)
