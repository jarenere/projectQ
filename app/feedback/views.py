from __future__ import division
from app import app, db
from flask import Blueprint, request, url_for, flash, redirect, abort, session, g
from flask import render_template
from flask.ext.login import login_user, logout_user, current_user, login_required
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionText
from app.models import StateSurvey
from app.models import Answer
from app.models import GameImpatience, GameLottery1, GameLottery2
from app.models import GameRent1, GameRent2, GameUltimatum, GameDictador
from app.models import Game
from sqlalchemy.sql import func
from wtforms import TextField, BooleanField, RadioField, IntegerField, HiddenField
from wtforms.validators import Required, Regexp, Optional
from wtforms import ValidationError
import datetime
from . import blueprint
from app.decorators import valid_survey, there_is_stateSurvey,finished_survey
from ..main.errors import ErrorEndDateOut, ErrorExceeded, ErrorTimedOut
from app.decorators import researcher_required, belong_researcher
from sqlalchemy import or_
from config import basedir





@blueprint.route('/<int:id_survey>', methods=['GET', 'POST'])
@blueprint.route('/<int:id_survey>/<int:feedback>', methods=['GET', 'POST'])
@login_required
@finished_survey
def logic_feedback(id_survey,feedback=0):
    '''Function that decides which is the next step in the survey
    '''    
    list_date=[]
    list_date.append((get_date_decision1(current_user.id,id_survey),"decision1"))
    list_date.append((get_date_decision("decision_two",current_user.id,id_survey),"decision2"))
    list_date.append((get_date_decision("decision_three",current_user.id,id_survey),"decision3"))
    list_date.append((get_date_decision("decision_four",current_user.id,id_survey),"decision4"))
    list_date.append((get_date_decision("decision_six",current_user.id,id_survey),"decision6"))
    list_date.sort(cmp=lambda a,b: cmp(a[0],b[0]))
    if request.method == 'POST':
        feedback=feedback+1
        return redirect(url_for('feedback.logic_feedback',id_survey = id_survey, feedback = feedback))
    if feedback >4:
        return render_template('/feedback/index.html',
                id_survey=id_survey,
                tittle = "feedback"
                )

    decision = list_date[feedback][1]
    if decision == "decision1":
        return decision1(id_survey = id_survey)
    elif decision =="decision2":
        return decision2(id_survey = id_survey)
    elif decision =="decision3":
        return decision3(id_survey = id_survey)
    elif decision =="decision4":
        return decision4(id_survey = id_survey)
    elif decision =="decision6":
        return decision6(id_survey = id_survey)


@blueprint.route('/<int:id_survey>/decision1')
@login_required
@finished_survey
def decision1(id_survey):
    current_user.id = current_user.id
    decision1_v1=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==id_survey,\
            Question.decision=="decision_one_v1")

    ans1_v1=Answer.query.filter(\
            Answer.user_id==current_user.id,\
            or_(Answer.question==decision1_v1[0],Answer.question==decision1_v1[1])).first()
    if ans1_v1 is not None:
        ans1 = ans1_v1.answerNumeric
        decision1=decision1_v1
        f = open(basedir+"/app/static/feedback1_v1.re", "r")
        text =  f.read()
        f.close()
    else:
        decision1=Question.query.filter(\
                Question.section_id==Section.id,\
                Section.root_id==id_survey,\
                Question.decision=="decision_one_v2")

        ans1=Answer.query.filter(Answer.user_id==current_user.id,\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).\
                first().answerNumeric
        f = open(basedir+"/app/static/feedback1_v2.re", "r")
        text =  f.read()
        f.close()

    n1 = Answer.query.filter(\
            or_(Answer.question==decision1[0],Answer.question==decision1[1]),\
            Answer.answerNumeric==ans1).count()
    
    total1 = Answer.query.filter(\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).count()
    
    percent1 = n1/total1
    avg1 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision1[0],Answer.question==decision1[1])).first()[0] 

    return render_template('/feedback/feedback.html',
            tittle = "feedback",
            text = text,
            ans = ans1,
            avg = avg1,
            percent = percent1)


def get_percent(decision, user_id, survey_id):
    decisions=[q.id for q in Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==survey_id,\
            Question.decision==decision).all()]

    
    ans=Answer.query.filter(Answer.user_id==user_id,\
            Answer.question_id.in_(decisions)).first().answerNumeric

    n = Answer.query.filter(\
            Answer.question_id.in_(decisions),\
            Answer.answerNumeric==ans).count()
    
    total = Answer.query.filter(\
                Answer.question_id.in_(decisions)).count()
    
    percent = n/total
    avg = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        Answer.question_id.in_(decisions)).first()[0] 

    return ans, avg, percent





@blueprint.route('/<int:id_survey>/decision2')
@login_required
@finished_survey
def decision2(id_survey):

    ans,avg,percent = get_percent("decision_two", current_user.id,id_survey)
    f = open(basedir+"/app/static/feedback2.re", "r")
    text =  f.read()
    f.close()

    return render_template('/feedback/feedback.html',
            tittle = "feedback",
            text = text,
            ans = ans,
            avg = avg,
            percent = percent)

@blueprint.route('/<int:id_survey>/decision3')
@login_required
@finished_survey
def decision3(id_survey):

    ans,avg,percent = get_percent("decision_three", current_user.id,id_survey)
    f = open(basedir+"/app/static/feedback3.re", "r")
    text =  f.read()
    f.close()

    return render_template('/feedback/feedback.html',
            tittle = "feedback",
            text = text,
            ans = ans,
            avg = avg,
            percent = percent)

@blueprint.route('/<int:id_survey>/decision4')
@blueprint.route('/<int:id_survey>/decision4&5')
@login_required
@finished_survey
def decision4(id_survey):

    ans,avg,percent = get_percent("decision_four", current_user.id,id_survey)
    f = open(basedir+"/app/static/feedback4&5.re", "r")
    text =  f.read()
    f.close()

    all_decision5 =[q.id for q in Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==id_survey,\
            Question.decision=="decision_five").all()]

    decisions5 = [q.id for q in Question.query.filter(\
            Question.id.in_(all_decision5),\
            Question.choices==[str(ans)]).all()]

    n5 = Answer.query.filter(\
            Answer.question_id.in_(decisions5),\
            Answer.answerYN==True).count()
    total5 = Answer.query.filter(\
                Answer.question_id.in_(decisions5)).count()

    percent5 = n5/total5

    return render_template('/feedback/feedback.html',
            tittle = "feedback",
            text = text,
            ans = ans,
            avg = avg,
            percent = percent,
            percent5 = percent5)

@blueprint.route('/<int:id_survey>/decision6')
@login_required
@finished_survey
def decision6(id_survey):

    ans,avg,percent = get_percent("decision_six", current_user.id,id_survey)
    f = open(basedir+"/app/static/feedback6.re", "r")
    text =  f.read()
    f.close()

    return render_template('/feedback/feedback.html',
            tittle = "feedback",
            text = text,
            ans = ans,
            avg = avg,
            percent = percent)

def get_date_decision(decision, user_id,id_survey):
    '''return date when answered 
    '''
    return Answer.query.filter(Answer.user_id==user_id,\
            Answer.question_id==Question.id,\
            Question.section_id==Section.id,\
            Section.root_id==id_survey,\
            Question.decision==decision).first().created

def get_date_decision1(user_id,id_survey):
    '''return date when answered 
    '''
    return Answer.query.filter(Answer.user_id==user_id,\
            Answer.question_id==Question.id,\
            Question.section_id==Section.id,\
            Section.root_id==id_survey,\
            Question.decision.in_(["decision_one_v1","decision_one_v2"])).\
            first().created




