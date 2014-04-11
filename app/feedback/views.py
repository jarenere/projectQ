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
from app.decorators import valid_survey, there_is_stateSurvey
from ..main.errors import ErrorEndDateOut, ErrorExceeded, ErrorTimedOut
from app.decorators import researcher_required, belong_researcher
from sqlalchemy import or_



ID_SURVEY=1


@blueprint.route('/')
@blueprint.route('/index')
@blueprint.route('/<int:id_user>', methods=['GET', 'POST'])
@login_required
@researcher_required
def index(id_user=2):
    decision1_v1=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_one_v1")

    ans1_v1=Answer.query.filter(\
            Answer.user_id==id_user,\
            or_(Answer.question==decision1_v1[0],Answer.question==decision1_v1[1])).first()
    if ans1_v1 is not None:
        ans1 = ans1_v1.answerNumeric
        decision1=decision1_v1
    else:
        decision1=Question.query.filter(\
                Question.section_id==Section.id,\
                Section.root_id==ID_SURVEY,\
                Question.decision=="decision_one_v2")

        ans1=Answer.query.filter(Answer.user_id==id_user,\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).\
                first().answerNumeric

    n1 = Answer.query.filter(\
            or_(Answer.question==decision1[0],Answer.question==decision1[1]),\
            Answer.answerNumeric==ans1).count()
    
    total1 = Answer.query.filter(\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).count()
    
    percent1 = n1/total1
    avg1 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision1[0],Answer.question==decision1[1])).first()[0] 


    decision2=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_two")
    
    ans2=Answer.query.filter(Answer.user_id==id_user,\
            or_(Answer.question==decision2[0],Answer.question==decision2[1])).\
            first().answerNumeric
    
    n2 = Answer.query.filter(\
            or_(Answer.question==decision2[0],Answer.question==decision2[1]),\
            Answer.answerNumeric==ans2).count()
    
    total2 = Answer.query.filter(\
                or_(Answer.question==decision2[0],Answer.question==decision2[1])).count()
    
    percent2 = n2/total2
    avg2 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision2[0],Answer.question==decision2[1])).first()[0] 


    decision3=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_three")
    ans3=Answer.query.filter(\
            Answer.user_id==id_user,\
            or_(Answer.question==decision3[0],Answer.question==decision3[1])).first().answerNumeric
    
    n3 = Answer.query.filter(\
            or_(Answer.question==decision3[0],Answer.question==decision3[1]),\
            Answer.answerNumeric==ans3).count()
    
    total3 = Answer.query.filter(\
                or_(Answer.question==decision3[0],Answer.question==decision3[1])).count()
    
    percent3 = n3/total3
    avg3 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision3[0],Answer.question==decision3[1])).first()[0]


    decision4=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_four")
    ans4=Answer.query.filter(\
            Answer.user_id==id_user,\
            or_(Answer.question==decision4[0],Answer.question==decision4[1])).first().answerNumeric
    
    n4 = Answer.query.filter(\
            or_(Answer.question==decision4[0],Answer.question==decision4[1]),\
            Answer.answerNumeric==ans4).count()
    
    total4 = Answer.query.filter(\
                or_(Answer.question==decision4[0],Answer.question==decision4[1])).count()
    
    percent4 = n4/total4
    avg4 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision4[0],Answer.question==decision4[1])).first()[0] 

    
    decision6=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_six")
    ans6=Answer.query.filter(\
            Answer.user_id==id_user,\
            or_(Answer.question==decision6[0],Answer.question==decision6[1])).first().answerNumeric
    
    n6 = Answer.query.filter(\
            or_(Answer.question==decision6[0],Answer.question==decision6[1]),\
            Answer.answerNumeric==ans6).count()
    
    total6 = Answer.query.filter(\
                or_(Answer.question==decision6[0],Answer.question==decision6[1])).count()
    
    percent6 = n6/total6
    avg6 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision6[0],Answer.question==decision6[1])).first()[0] 


    all_decision5 =[q.id for q in Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_five").all()]

    decision5 = Question.query.filter(\
            Question.id.in_(all_decision5),\
            Question.choices==[str(ans4)]).all()

    n5 = Answer.query.filter(\
            or_(Answer.question==decision5[0],Answer.question==decision5[1]),\
            Answer.answerYN==True).count()
    total5 = Answer.query.filter(\
                or_(Answer.question==decision5[0],Answer.question==decision5[1])).count()

    percent5 = n5/total5




    return render_template('/feedback/feedback.html',
        ans1 = ans1,
        avg1 = avg1,
        same1 = n1, 
        diff1 = total1-n1,  
        ans2 = ans2,
        avg2 = avg2,
        same2 = n2,   
        diff2 = total2-n2,  
        ans3 = ans3,
        avg3 = avg3,
        same3 = n3,   
        diff3 = total3-n3,  
        ans4 = ans4,
        avg4 = avg4,
        same4 = n4,   
        diff4 = total4-n4,  
        ans6 = ans6,
        avg6 = avg6,
        same5 = n5,   
        diff6 = total6-n6,         
        same6 = n6,   
        diff5 = total5-n5,  
        tittle = 'feedback')



@blueprint.route('/decision1_v1')
@blueprint.route('/<int:id_user>', methods=['GET', 'POST'])
@login_required
@researcher_required
def decision1_v1(id_user=2):
    decision1_v1=Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==ID_SURVEY,\
            Question.decision=="decision_one_v1")

    ans1_v1=Answer.query.filter(\
            Answer.user_id==id_user,\
            or_(Answer.question==decision1_v1[0],Answer.question==decision1_v1[1])).first()
    if ans1_v1 is not None:
        ans1 = ans1_v1.answerNumeric
        decision1=decision1_v1
    else:
        decision1=Question.query.filter(\
                Question.section_id==Section.id,\
                Section.root_id==ID_SURVEY,\
                Question.decision=="decision_one_v2")

        ans1=Answer.query.filter(Answer.user_id==id_user,\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).\
                first().answerNumeric

    n1 = Answer.query.filter(\
            or_(Answer.question==decision1[0],Answer.question==decision1[1]),\
            Answer.answerNumeric==ans1).count()
    
    total1 = Answer.query.filter(\
                or_(Answer.question==decision1[0],Answer.question==decision1[1])).count()
    
    percent1 = n1/total1
    avg1 = db.session.query(func.avg(Answer.answerNumeric)).filter(\
        or_(Answer.question==decision1[0],Answer.question==decision1[1])).first()[0] 
    
    return render_template('/feedback/feedback.html',
            ans1 = ans1,
            avg1 = avg1,
            same1 = n1, 
            diff1 = total1-n1)