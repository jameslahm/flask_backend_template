from . import db
from flask import current_app
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer

class Permission:
    NORMAL = 0x01
    ADMIN = 0x04


class RoleName:
    ADMIN = 'admin'
    NORMAL = 'normal'

# TODO:

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    permission = db.Column('permission',
                           db.Integer,
                           unique=False)
    name = db.Column('name',db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        for name in [RoleName.ADMIN, RoleName.NORMAL]:
            role = Role.query.filter_by(name=name).first()
            if role is None:
                if name == RoleName.ADMIN:
                    role = Role(permission=Permission.ADMIN, name=name)
                if name == RoleName.NORMAL:
                    role = Role(permission=Permission.NORMAL, name=name)
                db.session.add(role)
                db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(64), unique=True)
    username = db.Column('username', db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey(
        'roles.id'))
    password_hash = db.Column(
        'password_hash', db.String(128))
    confirmed = db.Column('confirmed', db.Boolean, default=False)
    avatar = db.Column('avatar', db.String(128))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(
                    permission=Permission.ADMIN).first()
            else:
                self.role = Role.query.filter_by(
                    permission=Permission.NORMAL).first()
            self.role_id = self.role.id

    def to_json(self):
        json_user = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'confirmed': self.confirmed,
            'role': self.role.name,
        }
        return json_user

    @property
    def password(self):
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = TimedJSONWebSignatureSerializer(
            current_app.config['SECRET_KEY'], expires_in=expiration)
        # TODO:
        return s.dumps({"id": self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            # TODO:
            id = s.loads(token.encode('utf-8')).get("id")
        except:
            return False
        return User.query.filter(User.id == id).first()

    @staticmethod
    def get_admin():
        return User.query.filter(User.email == current_app.config['FLASK_ADMIN']).first()

    @staticmethod
    def search_byusername(body):
        if body.get('username'):
            u_name = body.get('username')
        else:
            u_name = ''
        page = int(body['page'])+1 if body.get('page') else 1
        page_size = int(body['page_size']) if body.get('page_size') else 10
        pa = User.query.filter(User.username.contains(u_name))
        if body.get('order'):
            if body.get('order_by'):
                if body['order_by'] == 'username':
                    if body.get('order') == 'desc':
                        pa = pa.order_by(User.username.desc())
                    else:
                        pa = pa.order_by(User.username.asc())
                if body['order_by'] == 'id':
                    if body.get('order') == 'desc':
                        pa = pa.order_by(User.id.desc())
                    else:
                        pa = pa.order_by(User.id.asc())
        pa = pa.paginate(
            int(page), int(page_size), error_out=False
        )
        return pa.items, pa.total

    @staticmethod
    def update_userinfo(id, user_now, body: dict):
        user_update = User.query.filter(User.id == id).first()
        if user_now and user_update:
            if body.get('username'):
                user_update.username = body.get('username')
            if body.get('password'):
                user_update.password = body.get('password')
            if body.get('avatar'):
                user_update.avatar = body.get('avatar')

            if user_now.role.permission == Permission.ADMIN:
                if body.get('confirmed') == True or body.get('confirmed') == False:
                    user_update.confirmed = body['confirmed']
                if body.get('role'):
                    user_update.role = Role.query.filter_by(
                        name=body['role']).first()
                    user_update.role_id = user_update.role.id
        else:
            return None
        db.session.commit()
        return user_update

    @staticmethod
    def delete_user(id, user_now):
        user_delete = User.query.filter(User.id == id).first()
        if user_now and user_delete:
            if user_now.role.permission == Permission.ADMIN:
                record = user_delete.to_json()
                db.session.delete(user_delete)
                db.session.commit()
                return record
        else:
            return None