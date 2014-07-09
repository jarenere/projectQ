from app import app, db, lm
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginFormOpenID, RegistrationForm, LoginFormEmail, RegistrationForm2
from . import blueprint
from ..models import User, ROLE_USER
from flask.ext.babel import gettext



# @blueprint.route('/login', methods=['GET', 'POST'])
# @blueprint.route('/', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     """
#     login method for users.

#     Returns a Jinja2 template with the result of signing process.

#     """
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('main.index'))
#     form = LoginFormOpenID()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
#     return render_template('/auth/login.html', 
#         title = 'Sign In',
#         form = form,
#         providers = app.config['OPENID_PROVIDERS'])

@blueprint.route('/login', methods=['GET', 'POST'])
@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/login-email', methods=['GET', 'POST'])
def login_email():
    form = LoginFormEmail()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(gettext('Invalid email or password.'))
    return render_template('auth/loginEmail.html', form=form)

# @blueprint.route('/register2', methods=['GET', 'POST'])
# def register2():
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         user = User(email=form.email.data,
#                     password=form.email.data)
#         db.session.add(user)
#         db.session.commit()
#         # token = user.generate_confirmation_token()
#         # send_email(user.email, 'Confirm Your Account',
#         #            'auth/email/confirm', user=user, token=token)
#         flash(gettext('A password has been sent to you by email.'))
#         return redirect(url_for('auth.login'))
#     return render_template('auth/register.html', form=form)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm2()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        # token = user.generate_confirmation_token()
        # send_email(user.email, 'Confirm Your Account',
        #            'auth/email/confirm', user=user, token=token)
        # flash(gettext('A password has been sent to you by email.'))
        login_user(user, True)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@blueprint.before_app_request
def before_request():
    # g.user = current_user
    if current_user.is_authenticated():
        g.user = current_user # return username in get_id()
    else:
        g.user = None # or 'some fake value', whatever



# @oid.after_login
# def after_login(resp):
#     if resp.email is None or resp.email == "":
#         flash(gettext('Invalid login. Please try again.'))
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email = resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
#         db.session.add(user)
#         db.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember = remember_me)
#     return redirect(request.args.get('next') or url_for('main.index'))
