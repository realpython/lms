# project/server/models.py


import datetime

from project.server import db, bcrypt


course_student_association_table = db.Table(
    'course_student_association',
    db.metadata,
    db.Column('student_id', db.Integer, db.ForeignKey('students.id')),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'))
)


class Course(db.Model):

    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    teacher_id = db.Column(
        db.Integer, db.ForeignKey('teachers.id'), nullable=False
    )
    teacher = db.relationship('Teacher', backref='courses')
    students = db.relationship(
        'Student',
        secondary=course_student_association_table,
        backref='courses'
    )

    def __init__(self, name, description, subject,
                 start_date, end_date, teacher_id):
        self.name = name
        self.description = description
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date
        self.teacher_id = teacher_id

    def __repr__(self):
        return '<Class {0}>'.format(self.name)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    user_role = db.Column(db.String(15))

    __mapper_args__ = {
        'polymorphic_identity': 'users',
        'polymorphic_on': user_role
    }

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_student(self):
        if self.user_role == 'student':
            return True
        else:
            return False

    def is_teacher(self):
        if self.user_role == 'teacher':
            return True
        else:
            return False

    def is_admin(self):
        if self.user_role == 'admin':
            return True
        else:
            return False

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Student(User):

    __tablename__ = "students"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __repr__(self):
        return '<Student {0}>'.format(self.email)


class Teacher(User):

    __tablename__ = "teachers"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher'
    }

    def __repr__(self):
        return '<Teacher {0}>'.format(self.email)


class Admin(User):

    __tablename__ = "admins"

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self):
        return '<Admin {0}>'.format(self.email)
