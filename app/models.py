from . import db

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


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True, index=True)
    #
    # for 'referential integrity' and ooey-gooey orm-ness:
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    #
    def __repr__(self):
        return '<User %r>' % self.username
