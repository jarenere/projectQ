# -*- coding: utf-8 -*-
from app import app, db
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from forms import LikertField, MyRadioField
from forms import generate_form
from utiles import generate_answer
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionText
from app.models import QuestionYN ,QuestionLikertScale
from app.models import StateSurvey
from app.models import Answer
from app.models import Raffle
from app.models import GameImpatience
from app.models import GameLottery1, GameLottery2, GameRent1, GameRent2, GameUltimatum, GameDictador
from sqlalchemy.sql import func
import datetime
from . import blueprint
from app.decorators import valid_survey, there_is_stateSurvey
from ..main.errors import ErrorEndDateOut, ErrorExceeded, ErrorTimedOut
from app.game.game import Games
from sqlalchemy import or_
from sqlalchemy import and_
from flask.ext.babel import gettext


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''
    shows all available surveys
    '''
    stmt1 = db.session.query(StateSurvey.survey_id, StateSurvey.status).\
        filter(StateSurvey.user==current_user).subquery()
    
    stmt2 = db.session.query(StateSurvey.survey_id, func.count('*').label('r_count')).\
        filter(StateSurvey.status.op('&')(StateSurvey.FINISH_OK)).\
        group_by(StateSurvey.survey_id).subquery()

    now = datetime.datetime.utcnow()
    #outerjoint Survey and StateSurvey(with the currentUser) and number of user
    # that have made the survey
    surveys = db.session.query(Survey, stmt1.c.status, stmt2.c.r_count).\
        outerjoin(stmt1,Survey.id==stmt1.c.survey_id).\
        outerjoin(stmt2,Survey.id==stmt2.c.survey_id).\
        filter(Survey.startDate<now,Survey.endDate>now).\
        order_by(Survey.startDate)
    return render_template('/surveys/index.html',
        title = 'Index',
        # surveys= [s.Survey for s in surveys],
        surveys = surveys) 

def info_games(id_survey):
    '''get info of game, raffle and impacience of the user
    '''
    raffle = Raffle.query.filter(Raffle.user_id==current_user.id,
        Raffle.survey_id==id_survey).first()
    part2 = GameImpatience.query.filter(GameImpatience.user_id==current_user.id,
        GameImpatience.survey_id==id_survey).first()
    lottery1 = GameLottery1.query.filter(GameLottery1.survey==id_survey,
        or_(and_(GameLottery1.userA==current_user.id,GameLottery1.repeatA==False),
            and_(GameLottery1.userB==current_user.id,GameLottery1.repeatB==False))).first()
    lottery2 = GameLottery2.query.filter(GameLottery2.survey==id_survey,
        or_(and_(GameLottery2.userA==current_user.id,GameLottery2.repeatA==False),
            and_(GameLottery2.userB==current_user.id,GameLottery2.repeatB==False))).first()
    rent1 = GameRent1.query.filter(GameRent1.survey==id_survey,
        or_(and_(GameRent1.userA==current_user.id,GameRent1.repeatA==False),
            and_(GameRent1.userB==current_user.id,GameRent1.repeatB==False))).first()
    rent2 = GameRent2.query.filter(GameRent2.survey==id_survey,
        or_(and_(GameRent2.userA==current_user.id,GameRent2.repeatA==False),
            and_(GameRent2.userB==current_user.id,GameRent2.repeatB==False))).first()
    ultimatum1 = GameUltimatum.query.filter(GameUltimatum.survey==id_survey,
        GameUltimatum.userA==current_user.id, GameUltimatum.repeatA==False).first()
    ultimatum2 = GameUltimatum.query.filter(GameUltimatum.survey==id_survey,
        GameUltimatum.userB==current_user.id, GameUltimatum.repeatB==False).first()
    dictador1 = GameDictador.query.filter(GameDictador.survey==id_survey,
        GameDictador.userA==current_user.id, GameDictador.repeatA==False).first()
    dictador2 = GameDictador.query.filter(GameDictador.survey==id_survey,
        GameDictador.userB==current_user.id, GameDictador.repeatB==False).first()
    return render_template('/surveys/results.html',
        title = "Resutls",
        user_id = current_user.id,
        raffle = raffle,
        part2 = part2,
        lottery1 = lottery1,
        lottery2 = lottery2,
        rent1 = rent1,
        rent2 = rent2,
        ultimatum1 = ultimatum1,
        ultimatum2 = ultimatum2,
        dictador1 = dictador1,
        dictador2 = dictador2)


def get_stateSurvey_or_error(id_survey,user,ip = None):
    stateSurvey, status = StateSurvey.getStateSurvey(id_survey,user,ip)
    if status == StateSurvey.NO_ERROR:
        return stateSurvey
    else:
        if status == StateSurvey.ERROR_EXCEEDED:
            raise ErrorExceeded
        if status == StateSurvey.ERROR_TIMED_OUT:
            raise ErrorTimedOut
        if status == StateSurvey.ERROR_END_DATE_OUT:
            raise ErrorEndDateOut
        if status == StateSurvey.ERROR_NO_SURVEY:
            return abort(404)
        return abort(500)    

def check_feedback(id_survey):
    '''check if survey have feedback
    '''
    ans = Answer.query.filter(Answer.user_id==current_user.id,
        Answer.question_id==Question.id,
        Question.section_id==Section.id, 
        Section.root_id==id_survey,
        Question.container==["feedback"]).first()
    if ans is not None:
        if ans.answerYN:
            return redirect(url_for('feedback.logic_feedback', id_survey = id_survey))

            # return render_template('/surveys/finish.html', 
            #     title = 'Finish')
    return render_template('/surveys/finish.html', 
        title = 'Finish')

def run_part2_raffle(id_survey):
    '''run part2 and raffle if user no always game with untrue money
    '''
    if id_survey==1:
        game = Games(id_survey)
        ss = StateSurvey.query.filter(StateSurvey.survey_id==id_survey,
            StateSurvey.user_id==current_user.id).first()
        if (ss.status & StateSurvey.FINISH_OK) and \
            (ss.status & StateSurvey.PART2_MONEY)==0 and \
            (ss.status & StateSurvey.PART2_NO_MONEY)==0:
            game.part2(current_user)
            game.raffle(current_user)


@login_required
@blueprint.route('/survey/<int:id_survey>', methods=['GET', 'POST'])
@valid_survey
def logicSurvey(id_survey):
    '''
    Function that decides which is the next step in the survey
    '''
    stateSurvey = get_stateSurvey_or_error(id_survey,g.user,request.remote_addr)

    if (stateSurvey.consented == False):
        return redirect(url_for('surveys.showConsent', id_survey = id_survey))
    section = stateSurvey.nextSection()
    if section is None:
        if stateSurvey.status & StateSurvey.FINISH_OK:
            run_part2_raffle(id_survey)
            return check_feedback(id_survey)
        if stateSurvey.status & StateSurvey.TIMED_OUT:
            return render_template('/survey/error_time_date.html',
                title ='time out')
        if stateSurvey.status & StateSurvey.END_DATE_OUT:
            return render_template('/survey/error_time_date.html',
                title ='End date out')
        print "\n raro\n Status: ", stateSurvey.status
        return abort(500) 
    return redirect (url_for('surveys.showQuestions',id_survey=id_survey,id_section=section.id))

@login_required
@blueprint.route('/survey/<int:id_survey>/consent', methods=['GET', 'POST'])
@blueprint.route('/survey/<int:id_survey>/consent/<int:n_consent>', methods=['GET', 'POST'])
@valid_survey
@there_is_stateSurvey
def showConsent(id_survey,n_consent = 0):
    '''
    Show consent, n_consent is the "position of consent", no id!!
    '''
    
    survey = Survey.query.get(id_survey)
    consents = survey.consents

    if n_consent>consents.count():
        abort (404)

    if consents.count()==0:
        stateSurvey = get_stateSurvey_or_error(id_survey,g.user)
        stateSurvey.accept_consent()
        return redirect(url_for('surveys.logicSurvey',id_survey = id_survey))
    
    if request.method == 'POST' and consents.count()<=n_consent+1:
        stateSurvey = get_stateSurvey_or_error(id_survey,g.user)
        stateSurvey.accept_consent()
        return redirect(url_for('surveys.logicSurvey',id_survey = id_survey))

    if request.method == 'POST' and consents.count()>n_consent+1:
        return redirect(url_for('surveys.showConsent', id_survey = id_survey, n_consent = n_consent+1))


    return render_template('/surveys/consent.html',
        title = survey.title,
        survey = survey,
        consent = survey.consents[n_consent])




def writeQuestion(question, form):
    '''return true if it isn't a subquestion or
        if a question.parent is valid
    '''
    if question.parent is None:
        return True
    else:
        data = form["c"+str(question.parent.id)].data
        if isinstance (question.parent,QuestionYN):
            if data.lower()==question.condition.value.lower():
                return True
            else:
                return False
        if isinstance (question.parent,QuestionText) or\
         isinstance(question.parent,QuestionChoice):
            if question.condition.operation=="<":
                if data<question.condition.value:
                    return True
                else:
                    return False
            if question.condition.operation=="==":
                if data==question.condition.value:
                    return True
                else:
                    return False
            if question.condition.operation==">":
                if int(data)>int(question.condition.value):
                    return True
                else:
                    return False


@login_required
@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>', methods=['GET', 'POST'])
@valid_survey
@there_is_stateSurvey
def showQuestions(id_survey, id_section):
    '''
    Show all question of a section
    '''
    stateSurvey = get_stateSurvey_or_error(id_survey,g.user,request.remote_addr)
    section = stateSurvey.nextSection()
    if section is None or section.id !=id_section:
        flash (gettext("access denied"))
        return abort (403)
        
    survey = Survey.query.get(id_survey)
    section = Section.query.get(id_section)
    questions = section.questions
   
    form = generate_form(questions)
    if form.validate_on_submit():
        for question in questions:
            if writeQuestion(question, form):
                answer = generate_answer(question,form,g.user)
            db.session.add(answer)
        db.session.commit()
        stateSurvey.finishedSection(form.time.data)
        return redirect(url_for('surveys.logicSurvey',id_survey = id_survey))

    return render_template('/surveys/showQuestions.html',
            title = survey.title,
            survey = survey,
            section = section,
            # form = form,
            form = form,
            questions = questions,
            percent = stateSurvey.percentSurvey()
            )
