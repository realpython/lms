# project/server/student/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user
from sqlalchemy import exc

from project.server import db
from project.server.student.forms import AddCourseForm
from project.server.models import Course, Student


##########
# config #
##########

student_blueprint = Blueprint('student', __name__,)


###########
# helpers #
###########

def get_all_courses():
    return Course.query.all()


def get_single_course(course_id):
    return Course.query.filter_by(id=course_id).first()


def get_single_course_name(course_name):
    return Course.query.filter_by(name=course_name).first()


def get_student(user_id):
    return Student.query.filter_by(id=user_id).first()


def get_available_courses(user_id):
    student_courses = get_student(user_id).courses
    return list(set(get_all_courses()) - set(student_courses))


def validate_student(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_student() is False:
            flash(
                'You do not have the correct permissions to view that page.',
                'warning'
            )
            return redirect(url_for('user.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


##########
# routes #
##########


@student_blueprint.route('/student/courses')
@login_required
@validate_student
def show_courses():
    return render_template('/student/courses.html')


@student_blueprint.route('/student/course/<int:course_id>')
@login_required
@validate_student
def show_single_course(course_id):
    return render_template(
        '/student/description.html',
        single_course=get_single_course(course_id)
    )


@student_blueprint.route(
    '/student/add_course',
    methods=['GET', 'POST']
)
@login_required
@validate_student
def add_course():
    available_courses = get_available_courses(current_user.get_id())
    if available_courses:
        form = AddCourseForm(request.form)
        form.courses.choices = [
            (single_course.name, single_course.name)
            for single_course in available_courses
        ]
        if form.validate_on_submit():
            course = get_single_course_name(form.courses.data)
            user = Student.query.filter_by(id=current_user.get_id()).first()
            course.students.append(user)
            try:
                db.session.commit()
                flash('Thank you for adding a new course.', 'success')
                return redirect('/student/courses')
            except exc.SQLAlchemyError:
                flash('Something went wrong.', 'danger')
                return redirect('/student/courses')
        return render_template('/student/add.html', form=form)
    else:
        flash('No new courses at this time.', 'warning')
        return render_template('/student/add.html')
