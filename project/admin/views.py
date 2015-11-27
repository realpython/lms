# project/admin/views.py


###########
# imports #
###########

from functools import wraps
from flask import render_template, Blueprint, request, flash, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user

from project.models import Course


##########
# config #
##########

admin_blueprint = Blueprint('admin', __name__,)


###########
# helpers #
###########

def get_courses():
    return Course.query.all()


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
