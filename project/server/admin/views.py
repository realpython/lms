# project/server/admin/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, \
    url_for, jsonify
from flask.ext.login import login_required
from flask.ext.login import current_user
from sqlalchemy import exc

from project.server import db
from project.server.models import Course, Teacher, Student
from project.server.admin.forms import UpdateCourseForm, AddCourseForm, \
    UpdateStudentForm, AddStudentForm, AddTeacherForm, UpdateTeacherForm


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


def get_single_student_by_email(student_email):
    return Student.query.filter_by(email=student_email).first()


def get_single_teacher(teacher_id):
    return Teacher.query.filter_by(id=teacher_id).first()


def get_available_students(course_id):
    """
    This function returns a list of students
    not currently taking a specific course
    """
    course = Course.query.filter_by(id=course_id).first()
    return list(set(get_students()) - set(course.students))


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
        students=get_students(),
        teachers=get_teachers()
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
    form.students.choices = [
        (students.email, students.email)
        for students in get_students()
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
        if form.students.data:
            for student_email in form.students.data:
                new_student = get_single_student_by_email(student_email)
                new_course.students.append(new_student)
        try:
            db.session.add(new_course)
            db.session.commit()
            flash('Thank you for adding a new course.', 'success')
            return redirect('/admin/dashboard')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard')
    return render_template('/admin/add_course.html', form=form)


@admin_blueprint.route(
    '/admin/update_course/<int:course_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_course(course_id):
    current_students = False
    potential_students = False
    form = UpdateCourseForm(request.form)
    form.teachers.choices = [
        (teacher.email, teacher.email)
        for teacher in get_teachers()
    ]
    course = get_single_course(course_id)
    if course.students:
        form.current_students.choices = [
            (students.email, students.email)
            for students in course.students
        ]
        current_students = True
    available_students = get_available_students(course_id)
    if available_students:
        form.potential_students.choices = [
            (students.email, students.email)
            for students in available_students
        ]
        potential_students = True
    if form.validate_on_submit():
        update_course = course
        update_course.name = form.name.data
        update_course.description = form.description.data
        update_course.subject = form.subject.data
        update_course.start_date = form.start_date.data
        update_course.end_date = form.end_date.data
        update_course.teacher_id = get_teacher_id(form.teachers.data)
        if form.potential_students.data:
            for student_email in form.potential_students.data:
                new_student = get_single_student_by_email(student_email)
                update_course.students.append(new_student)
        if form.current_students.data:
            for student_email in form.current_students.data:
                student = get_single_student_by_email(student_email)
                update_course.students.remove(student)
        try:
            db.session.commit()
            flash('Course updated. Thank you', 'success')
            return redirect('/admin/dashboard'.format(course_id))
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard'.format(course_id))
    return render_template(
        '/admin/update_course.html',
        form=form,
        single_course=course,
        current_students=current_students,
        potential_students=potential_students
    )


@admin_blueprint.route(
    '/admin/course/<int:course_id>',
    methods=['DELETE']
)
@login_required
@validate_admin
def delete_course(course_id):
    course = get_single_course(course_id)
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({'status': '{0} removed!'.format(course.name)})
    except exc.SQLAlchemyError:
        return jsonify({'status': 'Something went wrong.'})


@admin_blueprint.route(
    '/admin/add_student',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def add_student():
    form = AddStudentForm(request.form)
    if form.validate_on_submit():
        new_student = Student(
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(new_student)
            db.session.commit()
            flash('Thank you for adding a new student.', 'success')
            return redirect('/admin/dashboard')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard')
    return render_template('/admin/add_student.html', form=form)


@admin_blueprint.route(
    '/admin/update_student/<int:student_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_student(student_id):
    form = UpdateStudentForm(request.form)
    student = get_single_student(student_id)
    if form.validate_on_submit():
        update_student = student
        update_student.email = form.email.data
        update_student.registered_on = form.registered_on.data
        try:
            db.session.commit()
            flash('Student updated. Thank you', 'success')
            return redirect('/admin/dashboard')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard')
    return render_template(
        '/admin/update_student.html',
        form=form,
        single_student=student
    )


@admin_blueprint.route(
    '/admin/student/<int:student_id>',
    methods=['DELETE']
)
@login_required
@validate_admin
def delete_student(student_id):
    student = get_single_student(student_id)
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'status': '{0} removed!'.format(student.email)})
    except exc.SQLAlchemyError:
        return jsonify({'status': 'Something went wrong.'})


@admin_blueprint.route(
    '/admin/add_teacher',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def add_teacher():
    form = AddTeacherForm(request.form)
    if form.validate_on_submit():
        new_teacher = Teacher(
            email=form.email.data,
            password=form.password.data
        )
        try:
            db.session.add(new_teacher)
            db.session.commit()
            flash('Thank you for adding a new teacher.', 'success')
            return redirect('/admin/dashboard')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard')
    return render_template('/admin/add_teacher.html', form=form)


@admin_blueprint.route(
    '/admin/update_teacher/<int:teacher_id>',
    methods=['GET', 'POST']
)
@login_required
@validate_admin
def update_teacher(teacher_id):
    form = UpdateTeacherForm(request.form)
    teacher = get_single_teacher(teacher_id)
    if form.validate_on_submit():
        update_teacher = teacher
        update_teacher.email = form.email.data
        update_teacher.registered_on = form.registered_on.data
        try:
            db.session.commit()
            flash('Teacher updated. Thank you', 'success')
            return redirect('/admin/dashboard')
        except exc.SQLAlchemyError:
            flash('Something went wrong.', 'danger')
            return redirect('/admin/dashboard')
    return render_template(
        '/admin/update_teacher.html',
        form=form,
        single_teacher=teacher
    )


@admin_blueprint.route(
    '/admin/teacher/<int:teacher_id>',
    methods=['DELETE']
)
@login_required
@validate_admin
def delete_teacher(teacher_id):
    teacher = get_single_teacher(teacher_id)
    try:
        db.session.delete(teacher)
        db.session.commit()
        return jsonify({'status': '{0} removed!'.format(teacher.email)})
    except exc.SQLAlchemyError:
        return jsonify({'status': 'Something went wrong.'})
