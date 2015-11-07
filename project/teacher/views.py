# project/teacher/views.py


###########
# imports #
###########

from flask import render_template, Blueprint, request, flash, redirect
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Class
from project.teacher.forms import AddClassForm

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


##########
# routes #
##########


@teacher_blueprint.route('/teacher/classes/')
@login_required
def show_classes():
    return render_template(
        '/teacher/classes.html', classes=get_classes(current_user.get_id())
    )


@teacher_blueprint.route(
    '/teacher/add_class/',
    methods=['GET', 'POST']
)
@login_required
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
        return redirect('/teacher/classes'.format(current_user.get_id()))
    return render_template('/teacher/class.html', form=form)


@teacher_blueprint.route('/teacher/class/<int:class_id>')
@login_required
def show_single_class(class_id):
    return render_template(
        '/teacher/class_description.html',
        single_class=get_single_class(class_id)
    )
