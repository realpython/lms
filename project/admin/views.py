# project/admin/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Course
from project.teacher.forms import UpdateCourseForm


##########
# config #
##########

admin_blueprint = Blueprint('admin', __name__,)


###########
# helpers #
###########

def get_courses():
    return Course.query.all()


def get_single_course(course_id):
    return Course.query.filter_by(id=course_id).first()


def validate_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_admin() is False:
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

@admin_blueprint.route('/admin/dashboard/')
@login_required
@validate_admin
def dashboard():
    return render_template('/admin/dashboard.html', courses=get_courses())


@admin_blueprint.route(
    '/admin/update_course/<int:course_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_course(course_id):
    form = UpdateCourseForm(request.form)
    if form.validate_on_submit():
        update_course = get_single_course(course_id)

        update_course.name = form.name.data
        update_course.description = form.description.data
        update_course.subject = form.subject.data
        update_course.start_date = form.start_date.data
        update_course.end_date = form.end_date.data

        db.session.commit()

        flash('Course updated. Thank you', 'success')
        return redirect('/admin/dashboard'.format(course_id))
    return render_template(
        '/admin/update.html',
        form=form,
        single_course=get_single_course(course_id)
    )
