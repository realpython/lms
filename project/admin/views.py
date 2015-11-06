# project/admin/views.py


###########
# imports #
###########

from flask import render_template, Blueprint
from flask.ext.login import login_required


##########
# config #
##########

admin_blueprint = Blueprint('admin', __name__,)


##########
# routes #
##########


@admin_blueprint.route('/admin/')
@login_required
def admin_home():
    return render_template('/admin/home.html')
