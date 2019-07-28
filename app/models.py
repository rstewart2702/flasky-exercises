from . import db

from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager

from flask_login import UserMixin

# flask-login will call the following function when it needs to retrieve
# information about the logged-in user.  The decorator ensures that
# the function is registered with flask-login:
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Database-related classes:
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #
    # for "referential integrity" and for ooey-gooey orm-ness:
    users = db.relationship('User', backref = 'role', lazy='dynamic')
    #
    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #
    #
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    # Password hashing function is implemented through a "write-only"
    # property called password:
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # Method verify_password takes a password and uses
    # Werkzeug's check_password_hash for verification against hashed
    # versoin stored in the User model.
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    
    #
    # for 'referential integrity' and ooey-gooey orm-ness:
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #
    def __repr__(self):
        return '<User %r>' % self.username

