# -*- coding: utf-8 -*-
from app import app, db, lm, oid
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionNumerical, QuestionText
from app.models import QuestionYN


blueprint = Blueprint('account', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''
    shows all available surveys
    '''
    surveys = Survey.query.all()
    return render_template('/account/index.html',
        title = 'Index',
        surveys = surveys)



@blueprint.route('/login', methods=['GET', 'POST'])
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
    return render_template('/account/login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])


@blueprint.route('/survey/<int:id_survey>', methods=['GET', 'POST'])
@login_required
def logicSurvey(id_survey):
    '''
    Function that decides which is the next step in the survey
    '''
    survey = Survey.query.get(id_survey)
    if (g.get('consent', None)) == (None) or (g.get('consent', None) == False):
        return showConsent(id_survey)
    return redirect (url_for('account.index'))

def showConsent(id_survey):
    '''
    Show consent
    '''
    if request.method == 'POST':
        g.consent = True
        return redirect(url_for('account.logicSurvey',id_survey = id_survey))
    survey = Survey.query.get(id_survey)
    return render_template('/account/consent.html',
        title = survey.title,
        survey = survey,
        consent = survey.consents.first())