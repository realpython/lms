# project/teacher/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Class
from project.teacher.forms import AddClassForm, UpdateClassForm


##########
# config #
##########

teacher_blueprint = Blueprint('teacher', __name__,)


###########
# helpers #
###########

def get_classes(user_id):
    return Class.query.filter_by(user_id=user_id).all()


def get_single_class(class_id):
    return Class.query.filter_by(id=class_id).first()


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


@teacher_blueprint.route('/teacher/classes')
@login_required
@validate_teacher
def show_classes():
    return render_template(
        '/teacher/classes.html', classes=get_classes(current_user.get_id())
    )


@teacher_blueprint.route('/teacher/class/<int:class_id>')
@login_required
@validate_teacher
def show_single_class(class_id):
    return render_template(
        '/teacher/description.html',
        single_class=get_single_class(class_id)
    )


@teacher_blueprint.route(
    '/teacher/add_class',
    methods=['GET', 'POST']
)
@login_required
@validate_teacher
def add_class():
    form = AddClassForm(request.form)
    if form.validate_on_submit():
        new_class = Class(
            name=form.name.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            user_id=current_user.get_id()
        )
        db.session.add(new_class)
        db.session.commit()

        flash('Thank you for adding a new class.', 'success')
        return redirect('/teacher/classes')
    return render_template('/teacher/add.html', form=form)


@teacher_blueprint.route(
    '/teacher/update_class/<int:class_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_teacher
def update_class(class_id):
    form = UpdateClassForm(request.form)
    if form.validate_on_submit():
        update_class = get_single_class(class_id)

        update_class.name = form.name.data
        update_class.description = form.description.data
        update_class.start_date = form.start_date.data
        update_class.end_date = form.end_date.data

        db.session.commit()

        flash('Class updated. Thank you', 'success')
        return redirect('/teacher/class/{0}'.format(class_id))
    return render_template(
        '/teacher/update.html',
        form=form,
        single_class=get_single_class(class_id)
    )
