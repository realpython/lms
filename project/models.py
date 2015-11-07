# project/models.py


import datetime

from project import db, bcrypt


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    student = db.Column(db.Boolean, nullable=False, default=True)
    teacher = db.Column(db.Boolean, nullable=False, default=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    classes_taught = db.relationship(
        'Class', backref='person', lazy='dynamic'
    )

    def __init__(self, email, password, student=True,
                 teacher=False, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.registered_on = datetime.datetime.now()
        self.student = student
        self.teacher = teacher
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_student(self):
        if self.student:
            return True
        else:
            return False

    def is_teacher(self):
        if self.teacher:
            return True
        else:
            return False

    def is_admin(self):
        if self.admin:
            return True
        else:
            return False

    def __repr__(self):
        return '<User {0}>'.format(self.email)


class Class(db.Model):

    __tablename__ = "classes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    description = db.Column(db.Text(), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, description, start_date, end_date, user_id):
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.user_id = user_id

    def __repr__(self):
        return '<Class {0}>'.format(self.name)
