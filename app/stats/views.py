from app import app, db
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionText
from app.models import StateSurvey, User
from app.models import Answer
from app.models import GameImpatience, GameLottery1, GameLottery2
from app.models import GameRent1, GameRent2, GameUltimatum, GameDictador
from app.models import Game
from app.models import Raffle
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
# from .matching import Games
from app.game.game import Games
import csv

ID_SURVEY=1

@blueprint.route('/usuarios')
@login_required
@researcher_required
def usuarios():
    n_total = len(User.query.all())
    n_start = StateSurvey.query.filter(StateSurvey.survey_id==1).count()
    n_finish = StateSurvey.query.filter(StateSurvey.status.op('&')(StateSurvey.FINISH_OK)).count()
    return render_template('/stats/usuarios.html',
        n_start = n_start,
        n_finish = n_finish,
        n_total = n_total,
        tittle = 'usuarios')
  
@blueprint.route('/premios')
@login_required
@researcher_required
def premios():
    n_finish = StateSurvey.query.filter(StateSurvey.status.op('&')(StateSurvey.FINISH_OK)).count()
    raffle = Raffle.query.filter(Raffle.prize!=0)
    gameA = Game.query.filter(Game.prizeA)
    gameB = Game.query.filter(Game.prizeB)
    impatience = GameImpatience.query.filter(GameImpatience.prize)
    sum_raffle = sum(r.prize for r in raffle)
    sum_decisions = sum (g.moneyA for g in gameA) + \
        sum (g.moneyB for g in gameB)
    sum_impatience =  sum (int(i.answer.answerText[8:10]) for i in impatience)
    sum_total =  sum_raffle + sum_decisions + sum_impatience
    return render_template('/stats/premios.html',
        n_finish = n_finish,
        sum_total = sum_total,
        sum_decisions = sum_decisions,
        sum_raffle = sum_raffle,
        sum_impatience = sum_impatience,
        raffle = raffle,
        gameA = gameA,
        gameB = gameB,
        impatience = impatience,
        tittle = 'premios')
  
@blueprint.route('/prueba_correo')
@login_required
@researcher_required
def prueba_correo():
    from app import email
    from app.models import User

    user1 = User.query.get(1)
    flash(app.debug)
    flash ("enviando correo")
    email.send_email('jarenere@gmail.com',"prueba","email/prueba", user=user1)
    return render_template('index.html')
@blueprint.route('/div')
@login_required
@researcher_required
def division_cero():
    5/0
    return render_template('index.html')


@blueprint.route('/')
@blueprint.route('/index')
@login_required
@researcher_required
def index():
    flash(app.debug)
    return render_template('/stats/index.html',
        tittle = 'stats')

@blueprint.route('/run')
@login_required
@researcher_required
def run():
    game = Games(1)
    #users = StateSurvey.query.filter(StateSurvey.survey_id==ID_SURVEY,\
        #StateSurvey.status.op('&')(StateSurvey.FINISH_OK))
    #for u in users:
        #game.part2_reimplement(u.user)
        # print u.user.id, u.user.email

    game.match()

    #for u in users:
        #game.raffle(u.user)
        # print u.id, u.user_id

    return redirect(url_for('stats.index'))

@blueprint.route('/raffle')
@login_required
@researcher_required
def raffle():
    # survey = Survey.query.get(1)
    # game = Games(survey)

    raffle = Raffle.query.filter(Raffle.survey_id==ID_SURVEY)

    return render_template('/stats/raffle.html',
        tittle = 'stats',
        raffle = raffle)



@blueprint.route('/part_two')
@login_required
@researcher_required
def part_two():
    # survey = Survey.query.get(1)
    # game = Games(survey)

    part2 =db.session.query(GameImpatience, Answer, Question, StateSurvey).filter(\
        GameImpatience.survey_id==ID_SURVEY,\
        GameImpatience.answer_id==Answer.id,\
        Answer.question_id==QuestionChoice.id,\
        StateSurvey.survey_id==ID_SURVEY,\
        StateSurvey.user_id==GameImpatience.user_id)

    return render_template('/stats/part_two.html',
        tittle = 'stats',
        part2 = part2)

@blueprint.route('/decision_one_v1')
@login_required
@researcher_required
def decision_one_v1():
    results = GameLottery1.query.filter(\
        GameLottery1.survey_id==ID_SURVEY)

    return render_template('/stats/decision_one_v1.html',
        tittle = 'stats',
        results = results)

@blueprint.route('/decision_one_v2')
@login_required
@researcher_required
def decision_one_v2():
    results = GameLottery2.query.filter(\
        GameLottery2.survey_id==ID_SURVEY)

    return render_template('/stats/decision_one_v2.html',
        tittle = 'stats',
        results = results)

@blueprint.route('/decision_two')
@login_required
@researcher_required
def decision_two():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    results = GameRent1.query.filter(\
        GameRent1.survey_id==ID_SURVEY)

    return render_template('/stats/decision_two.html',
        tittle = 'stats',
        results = results)

@blueprint.route('/decision_three')
@login_required
@researcher_required
def decision_three():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    results = GameRent2.query.filter(\
        GameRent2.survey_id==ID_SURVEY)

    return render_template('/stats/decision_three.html',
        tittle = 'stats',
        results = results)

@blueprint.route('/decision_four&five')
@login_required
@researcher_required
def decision_four_five():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    results = GameUltimatum.query.filter(\
        GameUltimatum.survey_id==ID_SURVEY)


    return render_template('/stats/decision_four_five.html',
        tittle = 'stats',
        results = results)

@blueprint.route('/decision_six')
@login_required
@researcher_required
def decision_six():
    # survey = Survey.query.get(1)
    # game = Games(survey)
    results = GameDictador.query.filter(\
        GameDictador.survey_id==ID_SURVEY)

    return render_template('/stats/decision_six.html',
        tittle = 'stats',
        results = results)
