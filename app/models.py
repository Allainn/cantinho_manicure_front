from flask_login import UserMixin
from . import login_manager

class User(UserMixin):
    def __init__(self, email=None, id=None, login=None, tp_user=None):
        self.email = email
        self.id = id
        self.login = login
        self.tp_user = tp_user

    def __repr__(self):
        return '<User %r>' % self.email

@login_manager.user_loader
def load_user(user_id):
    return User(id = user_id)
