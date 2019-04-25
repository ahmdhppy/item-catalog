# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length, Regexp
from models.models import Categories
"""

This python file contains all the existing forms for the web application.
"""


def get_category():
    return [(category.id, category.name)
            for category in Categories.query.all()]


class SigninForm(FlaskForm):

    username = StringField('Username', validators=[
                           InputRequired(), Length(min=6, max=50)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember Me')


class SignupForm(FlaskForm):

    name = StringField('Name', validators=[
                       InputRequired(), Length(min=1, max=50)])
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=6, max=50),
                           Regexp('^[a-z0-9_]*$', message="""The username must
                            contain onlylowercase letters,numbers,
                            and underscores!""")])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])


class ItemForm(FlaskForm):

    name = StringField('Name', validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()])
    category_id = SelectField('Category', coerce=int,
                              validators=[InputRequired()],
                              choices=get_category())
