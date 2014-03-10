# -*- coding: utf-8 -*-
from app import app, db, lm, oid
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
from wtforms import TextField, BooleanField, RadioField, IntegerField, HiddenField
from wtforms.validators import Required, Regexp, Optional



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
    stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)
    if (stateSurvey.consented == False):
        return redirect(url_for('account.showConsent', id_survey = id_survey))
    section = stateSurvey.nextSection()
    if section ==None:
        return render_template('/account/finish.html', 
            title = 'Finish')
    return redirect (url_for('account.showQuestions',id_survey=id_survey,id_section=section.id))
    # return redirect (url_for('account.index'))

@blueprint.route('/survey/<int:id_survey>/consent', methods=['GET', 'POST'])
@login_required
def showConsent(id_survey):
    '''
    Show consent
    '''
    if request.method == 'POST':
        stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)
        stateSurvey.consented=True
        db.session.add(stateSurvey)
        db.session.commit()
        return redirect(url_for('account.logicSurvey',id_survey = id_survey))
    survey = Survey.query.get(id_survey)
    return render_template('/account/consent.html',
        title = survey.title,
        survey = survey,
        consent = survey.consents.first())


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>', methods=['GET', 'POST'])
@login_required
def showQuestions(id_survey, id_section):
    '''
    Show all question of a section
    '''
    class AnswerForm(Form):
        time = HiddenField('time')

        
    survey = Survey.query.get(id_survey)
    section = Section.query.get(id_section)
    questions = section.questions

    # Answer.prueba = TextField('Prueba')
    #listID = ["c"+str(q.id) for q in questions]
    
    for question in questions:
        setattr(AnswerForm,"globalTimec"+str(question.id),HiddenField('globalTimec'+str(question.id)))
        setattr(AnswerForm,"differentialTimec"+str(question.id),HiddenField('differentialTimec'+str(question.id)))

        #added "c" to that the key is valid
        if isinstance (question,QuestionYN):
            setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                choices = [('Yes','Yes'),('No','No')],validators = [Required()]))
            #setattr(Answer,"c"+str(question.id),RadioField('Answer', choices = [('Yes','Yes'),('No','No')], validators = [Optional()]))
            #Answer["c"+str(question.id)].validators = False
        if isinstance (question,QuestionNumerical):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))

        if isinstance (question,QuestionText,):
            if question.regularExpression !="":
                setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                    validators=[Required(), Regexp(question.regularExpression,0,question.errorMessage)]))
            elif question.isNumber:
                setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))
            else:
                setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Required()]))

        if isinstance (question,QuestionChoice):
            #First element must be a string, otherwise fail to valid choice
            list = [(str(index),choice) for index, choice in enumerate(question.choices)]
            setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                choices = list,validators = [Required()]))

        if isinstance (question, QuestionLikertScale):
            list = [(str(index),index) for index in range(question.minLikert,question.maxLikert+1)]
            setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                choices = list,validators = [Required()]))


        if isinstance(question, QuestionPartTwo):
            list = [(str(index),choice) for index, choice in enumerate(question.choices)]
            setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                choices = list,validators = [Required()]))

        if isinstance (question, QuestionDecisionOne):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))

        if isinstance (question, QuestionDecisionTwo):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))

        if isinstance (question, QuestionDecisionThree):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))
        
        if isinstance (question, QuestionDecisionFour):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))

        if isinstance (question, QuestionDecisionFive):
            setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                choices = [('Yes','Yes'),('No','No')],validators = [Required()]))

        if isinstance (question, QuestionDecisionSix):
            setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))


    form = AnswerForm()


    if form.validate_on_submit():
        for question in questions:
            if isinstance (question,QuestionYN):
                answer = Answer (answerYN = (form["c"+str(question.id)].data=='Yes'), user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionNumerical):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionText):
                if question.isExpectedAnswer():
                    #searches if the question has been answered
                    answer = Answer.query.filter(Answer.user_id==g.user.id,
                        Answer.question_id==question.id)
                    if answer.count()!=1:
                        answer = Answer (answerText = form["c"+str(question.id)].data, user= g.user, question = question)
                        answer.globalTime = form["globalTimec"+str(question.id)].data
                        answer.differentialTime = form["differentialTimec"+str(question.id)].data     
                        db.session.add(answer)
                        db.session.commit()          
                    else:
                        answer = answer.first()
                        answer.answerText = form["c"+str(question.id)].data
                    if not answer.answerAttempt():
                        if answer.isMoreAttempt():
                            flash ("answer wrong")
                            return render_template('/account/showQuestions.html',
                                title = survey.title,
                                survey = survey,
                                section = section,
                                # form = form,
                                form = form,
                                questions = questions)
                else:
                    answer = Answer (answerText = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()


            if isinstance (question,QuestionChoice):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question, QuestionLikertScale):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()

            if isinstance(question,QuestionPartTwo):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionDecisionOne):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionDecisionTwo):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionDecisionThree):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionDecisionFour):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()
            if isinstance (question,QuestionDecisionFive):
                answer = Answer (answerYN = (form["c"+str(question.id)].data=='Yes'), user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()

            if isinstance (question,QuestionDecisionSix):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
                answer.differentialTime = form["differentialTimec"+str(question.id)].data
                db.session.add(answer)
                db.session.commit()


        stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)
        stateSurvey.finishedSection()
        return redirect(url_for('account.logicSurvey',id_survey = id_survey))


    return render_template('/account/showQuestions.html',
            title = survey.title,
            survey = survey,
            section = section,
            # form = form,
            form = form,
            questions = questions)




    


