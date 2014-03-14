from app import app, db, lm, oid
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from . import blueprint
from ..models import User, ROLE_USER


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    login method for users.

    Returns a Jinja2 template with the result of signing process.

    """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('/auth/login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@blueprint.before_app_request
def before_request():
    g.user = current_user

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('main.index'))