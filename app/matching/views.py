from app import app, db
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LoginForm, AnswerChoiceForm, AnswerNumericalForm, AnswerTextForm, AnswerYNForm
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionNumerical, QuestionText
from app.models import QuestionYN ,QuestionLikertScale, QuestionPartTwo, QuestionDecisionOne,\
  QuestionDecisionTwo, QuestionDecisionThree, QuestionDecisionFour, \
  QuestionDecisionFive, QuestionDecisionSix
from app.models import StateSurvey
from app.models import Answer
from flask.ext.wtf import Form
from sqlalchemy.sql import func
from wtforms import TextField, BooleanField, RadioField, IntegerField, HiddenField
from wtforms.validators import Required, Regexp, Optional
from wtforms import ValidationError
import datetime
from . import blueprint
from app.decorators import valid_survey, there_is_stateSurvey
from ..main.errors import ErrorEndDateOut, ErrorExceeded, ErrorTimedOut


@blueprint.route('/')
@blueprint.route('/index')
@login_required
@researcher_required
def index():
    surveys = Survey.query.filter(Survey.researcher==g.user).order_by(Survey.created.desc())
    return render_template('/researcher/index.html',
        tittle = 'Survey',
        surveys = surveys)