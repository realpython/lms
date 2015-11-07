# project/student/views.py


###########
# imports #
###########

from flask import render_template, Blueprint, request, flash, redirect
from flask.ext.login import login_required
from flask.ext.login import current_user

from project.models import Course
# from project.student.forms import AddCourseForm


##########
# config #
##########

student_blueprint = Blueprint('student', __name__,)


###########
# helpers #
###########

def get_courses(user_id):
    pass


##########
# routes #
##########


@student_blueprint.route('/student/courses')
@login_required
def show_courses():
    return render_template(
        '/student/courses.html'
    )


@student_blueprint.route(
    '/student/add_course',
    methods=['GET', 'POST']
)
@login_required
def add_course():
    form = AddCourseForm(request.form)
    if form.validate_on_submit():
        print('Something needs to happen here!')
        flash('Thank you for adding a new course.', 'success')
        return redirect('/student/courses')
    return render_template('/student/add.html', form=form)
