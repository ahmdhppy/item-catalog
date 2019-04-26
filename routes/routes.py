# -*- coding: utf-8 -*-
from flask_googlelogin import GoogleLogin
from app import app
from models.models import Users, Categories, Items
from flask_login import LoginManager, login_user,\
    login_required, logout_user, current_user
from flask import render_template, request, redirect, url_for, Response
from forms import SigninForm, SignupForm, ItemForm
from flask import jsonify
import dicttoxml

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'
googlelogin = GoogleLogin(app, login_manager)
"""
This python file includes all the existing URL routes
which are responsible for reading category
as well as create/write/delete for items along
with login, signup, google authentication, endpoint API and home page.
"""


@app.route('/oauth2callback')
@googlelogin.oauth2callback
def create_or_update_user(token, userinfo, **params):
    """
    This function is responsible for the sign in
    and sign up through Google accounts.
    The Google account ID is passed to us,
    it checks if the ID already exists if it does, then
    it will log the user in using that Google account,
     otherwise will create a new account for the user and then log them in.
    """
    user = Users.query.filter_by(username=userinfo['id']).first()
    if user:
        user.write({'name': userinfo['name']})
    else:
        user = Users.create(
            {'username': userinfo['id'],
             'name': userinfo['name'],
             'login_with_google': True
             })
    login_user(user)
    return redirect(url_for('home'))


@app.route('/')
@app.route('/home')
def home():
    """
    This function renders the homepage along with
     the Category and displays the latest created item.
    """
    categories_ids = Categories.query.all()
    item_ids = Items.query.order_by(Items.id.desc()).limit(10).all()
    return render_template(
        'home.html',
        categories_ids=categories_ids,
        item_ids=item_ids)


@app.route('/showcategory/<int:category_id>', methods=['GET'])
def showcategory(category_id):
    """
    This function renders and displays all items for a certain Category.
    """
    categories_ids = Categories.query.all()
    category_id = Categories.query.filter_by(id=category_id).first()
    if category_id:
        item_ids = Items.query.filter_by(
            category_id=category_id.id).order_by(
            Items.id.desc()).all()
        return render_template(
            'home.html',
            categories_ids=categories_ids,
            item_ids=item_ids,
            active_category_id=category_id)
    else:
        return redirect(url_for('home'))


@app.route('/edititem/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edititem(item_id):
    """
    This function renders and displays the edit view for an item.
    """
    print("asdasda")
    form = ItemForm()
    item_id = Items.query.filter_by(id=item_id).first()
    if item_id:
        if not current_user.is_authenticated() \
                or current_user.id != item_id.user_id:
            return redirect(
                url_for(
                    'showcategory',
                    category_id=item_id.category_id.id))
        if form.validate_on_submit():
            vals = form.data
            vals.pop('csrf_token', False)
            item_id.write(vals)
            return redirect(
                url_for(
                    'showcategory',
                    category_id=item_id.category_id))
        form.name.data = item_id.name
        form.description.data = item_id.description
        form.category_id.data = item_id.category_id
        return render_template('edititem.html', form=form, item_id=item_id)
    else:
        return redirect(url_for('home'))


@app.route('/deleteitem/<int:item_id>', methods=['GET', 'POST'])
@login_required
def deleteitem(item_id):
    """
    This is the action for deleting an item.
    """
    item_id = Items.query.filter_by(
        id=item_id).order_by(
        Items.id.desc()).first()
    if item_id:
        if not current_user.is_authenticated() \
                or current_user.id != item_id.user_id:
            return redirect(
                url_for(
                    'showcategory',
                    category_id=item_id.category_id))
        if request.method == 'POST':
            item_id.delete()
            return redirect(
                url_for(
                    'showcategory',
                    category_id=item_id.category_id))
        return render_template('deleteitem.html', item_id=item_id)
    else:
        return redirect(url_for('home'))


@app.route('/newitem', methods=['GET', 'POST'])
@login_required
def newitem():
    """
    This renders the form for item creation.
    """
    form = ItemForm()
    if form.validate_on_submit():
        vals = form.data
        vals.pop('csrf_token', False)
        vals['user'] = current_user
        item_id = Items.create(vals)
        return redirect(
            url_for(
                'showcategory',
                category_id=item_id.category_id))
    return render_template('newitem.html', form=form)


@app.route('/categories', methods=['GET'])
@app.route('/categories/<int:categ_id>', methods=['GET'])
def json_categories(categ_id=None):
    """
    This action generates the endpoint API
    for a single category or all of the categories.
    """
    if request.args.get('version') == '1':
        if categ_id:
            categories = Categories.query.filter_by(id=categ_id).all()
        else:
            categories = Categories.query.all()
        vals = {'categories': []}
        for i in categories:
            vals['categories'].append(i.serializable())
            vals['categories'][-1]['items'] = \
                [i.serializable()
                 for i in Items.query.filter_by(category_id=i.id).all()]
        if request.args.get('type') == 'json':
            return jsonify(vals)
        elif request.args.get('type') == 'xml':
            return Response(dicttoxml.dicttoxml(vals, attr_type=False),
                            mimetype='text/xml')
    msg = """Make sure the url contains two arguments 'version' and 'type'.
Currently there are two types 'josn' and 'xml' and one version '1'"""
    return Response(msg, mimetype='text/plain')


@app.route('/items', methods=['GET'])
@app.route('/items/<int:item_id>', methods=['GET'])
def json_item(item_id=None):
    """
    This action generates the endpoint API
    for a single item or all of the items.

    """
    if request.args.get('version') == '1':
        if item_id:
            items = Items.query.filter_by(id=item_id).all()
        else:
            items = Items.query.all()
        vals = {'Items': []}
        for i in items:
            vals['Items'].append(i.serializable())

        if request.args.get('type') == 'json':
            return jsonify(vals)
        elif request.args.get('type') == 'xml':
            return Response(dicttoxml.dicttoxml(vals, attr_type=False),
                            mimetype='text/xml')
    msg = """Make sure the url contains two arguments 'version' and 'type'.
Currently there are two types 'josn' and 'xml' and one version '1'"""
    return Response(msg, mimetype='text/plain')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This is the sign up action, which makes sure the username
    doesn't exist in order to create a new user with that username.
    """
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form = SignupForm()
    if form.validate_on_submit():
        if Users.check_if_user_exists(form.username.data):
            flash("A user with that username already exists!")
            return redirect(url_for('signup'))
        else:
            vals = form.data
            vals.pop('csrf_token', False)
            user_id = Users.create(vals)
            login_user(user_id)
            return redirect(url_for('home'))
    return render_template('signup.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    """
    The action that takes the ID of the user and browses/searches
    for it in the database. This function is used by the login manager.
    """
    return Users.browse(int(user_id))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    """
    This function renders the sign in form and makes sure
    that the entered username and password are correct.
    After they are checked it will login the user.
    """
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form = SigninForm()
    if form.validate_on_submit():
        user = Users.check_credentials(form.data)
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash("Invalid password or email. Please try again.")
            return redirect(url_for('signin'))
    return render_template(
        'signin.html', form=form, google_login_url=googlelogin.login_url(
            redirect_uri='http://localhost:5000/oauth2callback'))


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    """
    This is the logout action.
    """
    if current_user.is_authenticated():
        logout_user()
    return redirect(url_for('home'))
