# -*- coding: utf-8 -*-
from app import db
from passlib.context import CryptContext
from flask_login import UserMixin
default_crypt_context = CryptContext(['pbkdf2_sha512'])


class BaseModel(db.Model):
    """Base data  db.model for all objects"""
    __abstract__ = True

    def serializable(self):
        """
        Function that turns the record into JSON.
        """
        vals = {}
        db.columns = [m.key for m in self.__table__.columns]
        for i in db.columns:
            vals[i] = getattr(self, i)
        return vals

    @classmethod
    def create(cls, vals):
        """
        Function that creates a record with given values.
        """
        record = cls(**vals)
        db.session.add(record)
        db.session.commit()
        return record

    def write(self, vals):
        """
        Function that edits an existing record with new given values.
        """
        for key, value in vals.iteritems():
            setattr(self, key, value)
        db.session.add(self)
        db.session.commit()
        return True

    def delete(self):
        """
        Function that removes (deletes) the record from the database.
        """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def browse(cls, id):
        """
        Function that takes the id of the record
        and returns the related object.
        """
        return cls.query.filter_by(id=id).first()


class Users(BaseModel, UserMixin):
    """
        Users Class: Inherits base and contains user specific attributes.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(200))
    login_with_google = db.Column(db.Boolean, default=False)

    @classmethod
    def create(cls, vals):
        """
        On new user creation this function is called and creates
        an encrypted password for security.
        """
        vals['password_hash'] = cls.encrypt_password(vals.pop('password', ''))
        return super(Users, cls).create(vals)

    @classmethod
    def _crypt_context(cls):
        """
        This function is used to retrieve the tool which
        is used in encrypting the password for users.
        """
        return default_crypt_context

    def _check_credentials(self, password):
        """
        This is the function that checks that the password and
        username are correct and that they belong to each other.
        """
        valid_pass, replacement = self._crypt_context(
        ).verify_and_update(password, self.password_hash)
        if replacement is not None:
            self.password_hash = replacement
            db.session.add(self)
            db.session.commit()
        return valid_pass and self

    @classmethod
    def encrypt_password(cls, password):
        """
        This function takes the password and encrypts it.
        """
        return cls._crypt_context().encrypt(password)

    @classmethod
    def check_if_user_exists(cls, username):
        """
        This is the function that checks if the input username
         exists in the database or not.
        """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def check_credentials(cls, vals):
        """
        This function receives the username and searches for it
        in the database and checks that the password and username are correct.

        """
        user = cls.query.filter_by(username=vals.get(
            'username', ''), login_with_google=False).first()
        return user and user._check_credentials(vals.get('password', ''))


class Categories(BaseModel):
    """
        Categories Class: Inherits base and contains user specific attributes.
    """
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)


class Items(BaseModel):
    """
        Items Class: Inherits base and contains user specific attributes.
    """
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    categories = db.relationship(Categories)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
