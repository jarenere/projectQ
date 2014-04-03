from app import app, db
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import Survey, Consent, Section, Match
from app.models import Question, QuestionChoice, QuestionNumerical, QuestionText
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
from app.decorators import researcher_required, belong_researcher
from .matching import Games

ID_SURVEY=1

@blueprint.route('/')
@blueprint.route('/index')
@login_required
@researcher_required
def index():
    return render_template('/stats/index.html',
        tittle = 'stats')

@blueprint.route('/')
@blueprint.route('/run')
@login_required
@researcher_required
def run():
    game = Games(1)
    users = StateSurvey.query.filter(StateSurvey.survey_id==ID_SURVEY,\
        StateSurvey.status.op('&')(StateSurvey.PART_TWO_MONEY)==0,\
        StateSurvey.status.op('&')(StateSurvey.PART_TWO_WITHOUT_MONEY)==0)
    for u in users:
        game.part_two(u.user)
        print u.user.id, u.user.nickname

    game.matching()

    return render_template('/stats/index.html',
        tittle = 'stats')


@blueprint.route('/part_two')
@login_required
@researcher_required
def part_two():
    # survey = Survey.query.get(1)
    # game = Games(survey)

    matchs2 =db.session.query(Match, Answer, Question, StateSurvey).filter(\
        Match.type=="part_two",\
        Match.survey==ID_SURVEY,\
        Match.answerA==Answer.id,\
        Answer.question_id==QuestionChoice.id,\
        StateSurvey.survey_id==ID_SURVEY,\
        StateSurvey.user_id==Match.userA)

    return render_template('/stats/part_two.html',
        tittle = 'stats',
        matchs2 = matchs2)

@blueprint.route('/decision_one')
@login_required
@researcher_required
def decision_one():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    matchs =Match.query.filter(\
        Match.type=="decision_one",\
        Match.survey==ID_SURVEY)

    return render_template('/stats/decision_one.html',
        tittle = 'stats',
        matchs = matchs)

@blueprint.route('/decision_two')
@login_required
@researcher_required
def decision_two():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    matchs =Match.query.filter(\
        Match.type=="decision_two",\
        Match.survey==ID_SURVEY)

    return render_template('/stats/decision_two.html',
        tittle = 'stats',
        matchs = matchs)

@blueprint.route('/decision_three')
@login_required
@researcher_required
def decision_three():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    matchs =Match.query.filter(\
        Match.type=="decision_three",\
        Match.survey==ID_SURVEY)

    return render_template('/stats/decision_three.html',
        tittle = 'stats',
        matchs = matchs)

@blueprint.route('/decision_four&five')
@login_required
@researcher_required
def decision_four_five():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    matchs =Match.query.filter(\
        Match.type=="decision_four",\
        Match.survey==ID_SURVEY)

    return render_template('/stats/decision_four_five.html',
        tittle = 'stats',
        matchs = matchs)

@blueprint.route('/decision_six')
@login_required
@researcher_required
def decision_six():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    matchs =Match.query.filter(\
        Match.type=="decision_six",\
        Match.survey==ID_SURVEY)

    return render_template('/stats/decision_six.html',
        tittle = 'stats',
        matchs = matchs)