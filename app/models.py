from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from datetime import datetime
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')
    
    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permission += perm
    
    def remove_permission(self,perm):
        if not self.has_permission(perm):
            self.permission -= perm
    
    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self,perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name



class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique = True, index = True)
    username = db.Column(db.String(64), unique=True, index=True)
    name = db.Column(db.String(64))
    location = db.Column(db.Text(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)


    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash, password)
    def generate_confirmation_token(self, expiration = 3600):
        s =Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm':self.id}).decode('utf-8')
    def confirm(self, token):
        s =Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
         return False
        self.confirmed = True
        db.session.add(self)
        return True
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
@staticmethod

def insert_roles():
    roles = {
        'User': [Permission.FOLLOW, Permission.COMMENT,Permission.COMMENT], 
        'Moderator': [Permission.FOLLOW, Permission.COMMENT, Permission.WRITE, Permission.MODERATE, 
                      ],
        'Administrator':[Permission.FOLLOW,Permission.COMMENT, Permission.WRITE,Permission.MODERATE,
                         Permission.ADMIN],
 
    }

    default_role = 'User'   
    for r in roles:
        role = Role.query.filter_by(name = r).first()
        if role is None:
            role = Role(name=r)
        role.reset_permissions()

        for perm in roles[r]:
            role.add_permission(perm)
            role.default = (role.name==default_role)
            db.session.add(role)
        db.session.commit()

        
 
    def __repr__(self):
        return '<User %r>' % self.username

