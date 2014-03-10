from app import app, db, lm, oid
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm





blueprint = Blueprint('auth', __name__)


@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    """
    login method for users.

    Returns a Jinja2 template with the result of signing process.

    """
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
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
    return redirect(url_for('index'))

