# project/admin/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, \
    url_for, jsonify
from flask.ext.login import login_required
from flask.ext.login import current_user

from project import db
from project.models import Course, Teacher, Student
from project.admin.forms import UpdateCourseForm, AddCourseForm, \
    UpdateStudentForm


##########
# config #
##########

admin_blueprint = Blueprint('admin', __name__,)


###########
# helpers #
###########

def get_courses():
    return Course.query.all()


def get_teachers():
    return Teacher.query.all()


def get_students():
    return Student.query.all()


def get_teacher_id(teacher_email):
    teacher_object = Teacher.query.filter_by(email=teacher_email).first()
    return teacher_object.id


def get_single_course(course_id):
    return Course.query.filter_by(id=course_id).first()


def get_single_student(student_id):
    return Student.query.filter_by(id=student_id).first()


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
    return render_template(
        '/admin/dashboard.html',
        courses=get_courses(),
        students=get_students()
    )


@admin_blueprint.route(
    '/admin/add_course',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def add_course():
    form = AddCourseForm(request.form)
    form.teachers.choices = [
        (teacher.email, teacher.email)
        for teacher in get_teachers()
    ]
    if form.validate_on_submit():
        new_course = Course(
            name=form.name.data,
            description=form.description.data,
            subject=form.subject.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            teacher_id=get_teacher_id(form.teachers.data)
        )
        db.session.add(new_course)
        db.session.commit()
        flash('Thank you for adding a new course.', 'success')
        return redirect('/admin/dashboard')
    return render_template('/admin/add.html', form=form)


@admin_blueprint.route(
    '/admin/update_course/<int:course_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_course(course_id):
    form = UpdateCourseForm(request.form)
    form.teachers.choices = [
        (teacher.email, teacher.email)
        for teacher in get_teachers()
    ]
    if form.validate_on_submit():
        update_course = get_single_course(course_id)
        update_course.name = form.name.data
        update_course.description = form.description.data
        update_course.subject = form.subject.data
        update_course.start_date = form.start_date.data
        update_course.end_date = form.end_date.data
        update_course.teacher_id = get_teacher_id(form.teachers.data)
        db.session.commit()
        flash('Course updated. Thank you', 'success')
        return redirect('/admin/dashboard'.format(course_id))
    return render_template(
        '/admin/update_course.html',
        form=form,
        single_course=get_single_course(course_id)
    )


@admin_blueprint.route(
    '/admin/course/<int:course_id>',
    methods=['DELETE']
)
@login_required
@validate_admin
def delete_course(course_id):
    course = get_single_course(course_id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({'test': 'test'})


@admin_blueprint.route(
    '/admin/update_student/<int:student_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_student(student_id):
    form = UpdateStudentForm(request.form)
    if form.validate_on_submit():
        update_student = get_single_student(student_id)
        update_student.email = form.email.data
        update_student.registered_on = form.registered_on.data
        db.session.commit()
        flash('Student updated. Thank you', 'success')
        return redirect('/admin/dashboard'.format(student_id))
    return render_template(
        '/admin/update_student.html',
        form=form,
        single_student=get_single_student(student_id)
    )
