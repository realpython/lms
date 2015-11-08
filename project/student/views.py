# project/student/views.py


###########
# imports #
###########

from flask import render_template, Blueprint, request, flash, redirect
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Course, User
from project.student.forms import AddCourseForm


##########
# config #
##########

student_blueprint = Blueprint('student', __name__,)


###########
# helpers #
###########

def get_courses(user_id):
    pass


def get_single_course(course_name):
    return Course.query.filter_by(name=course_name).first()


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
        course = get_single_course(form.courses.data)
        user = User.query.filter_by(id=current_user.get_id()).first()
        course.users.append(user)
        db.session.commit()
        flash('Thank you for adding a new course.', 'success')
        return redirect('/student/courses')
    return render_template('/student/add.html', form=form)
