from flask import Blueprint, redirect, url_for, request
from ..auth.models import db, User
from ..main.models import Post
from flask_admin.contrib.sqla import ModelView
from .. import admini
from flask_login import current_user
from flask import current_app as app

# Blueprint Configuration
admin_bp = Blueprint('admin_bp',
                    __name__,
                    template_folder='templates',
                    static_folder='static')

admin_user = app.config['ADMIN_USER']

class MyModelView(ModelView):
    def is_accessible(self):
        # return current_user.is_authenticated
        return (current_user.is_authenticated and
                current_user.name == admin_user)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth_bp.login', next=request.url))

admini.add_view(MyModelView(Post, db.session))
admini.add_view(MyModelView(User, db.session))

