# project/server/teacher/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required, current_user
from sqlalchemy import exc

from project.server import db
from project.server.models import Course
from project.server.teacher.forms import AddCourseForm, UpdateCourseForm


##########
# config #
##########

teacher_blueprint = Blueprint('teacher', __name__,)


###########
# helpers #
###########

def get_courses(user_id):
    return Course.query.filter_by(teacher_id=user_id).all()


def get_single_course(course_id):
    return Course.query.filter_by(id=course_id).first()


def validate_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_teacher() is False:
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


@teacher_blueprint.route('/teacher/courses')
@login_required
@validate_teacher
def show_courses():
    return render_template(
        '/teacher/courses.html', courses=get_courses(current_user.get_id())
    )


@teacher_blueprint.route('/teacher/course/<int:course_id>')
@login_required
@validate_teacher
def show_single_course(course_id):
    return render_template(
        '/teacher/description.html',
        single_course=get_single_course(course_id)
    )


@teacher_blueprint.route(
    '/teacher/add_course',
    methods=['GET', 'POST']
)
@login_required
@validate_teacher
def add_course():
    form = AddCourseForm(request.form)
    if form.validate_on_submit():
        new_course = Course(
            name=form.name.data,
            description=form.description.data,
            subject=form.subject.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            teacher_id=current_user.get_id()
        )
        try:
            db.session.add(new_course)
            db.session.commit()
            flash('Thank you for adding a new course.', 'success')
            return redirect('/teacher/courses')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/teacher/courses')
    return render_template('/teacher/add.html', form=form)


@teacher_blueprint.route(
    '/teacher/update_course/<int:course_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_teacher
def update_course(course_id):
    form = UpdateCourseForm(request.form)
    if form.validate_on_submit():
        update_course = get_single_course(course_id)
        update_course.name = form.name.data
        update_course.description = form.description.data
        update_course.subject = form.subject.data
        update_course.start_date = form.start_date.data
        update_course.end_date = form.end_date.data
        try:
            db.session.commit()
            flash('Course updated. Thank you', 'success')
            return redirect('/teacher/course/{0}'.format(course_id))
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/teacher/course/{0}'.format(course_id))
    return render_template(
        '/teacher/update.html',
        form=form,
        single_course=get_single_course(course_id)
    )
