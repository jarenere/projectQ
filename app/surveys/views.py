# -*- coding: utf-8 -*-
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
from app.main.errors import MyCustom600

from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, IntegerField, HiddenField
from wtforms.validators import Required, Regexp, Optional
from wtforms import ValidationError
import datetime
from . import blueprint





@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    '''
    shows all available surveys
    '''
    now = datetime.datetime.utcnow()
    surveys = Survey.query.filter(Survey.startDate<now,Survey.endDate>now).\
            order_by(Survey.startDate)
    return render_template('/surveys/index.html',
        title = 'Index',
        surveys = surveys)

@blueprint.route('/survey/<int:id_survey>', methods=['GET', 'POST'])
@login_required
def logicSurvey(id_survey):
    '''
    Function that decides which is the next step in the survey
    '''
    stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user,request.remote_addr)
    if not stateSurvey.check_survey_duration_and_date():
        flash ("access denied")
        raise MyCustom600

    if (stateSurvey.consented == False):
        return redirect(url_for('surveys.showConsent', id_survey = id_survey))
    section = stateSurvey.nextSection()
    if section ==None:
        if stateSurvey.status & StateSurvey.END_DATE_OUT or stateSurvey.status & StateSurvey.TIMED_OUT:
            flash ("access denied")
            raise MyCustom600
        else:
            return render_template('/surveys/finish.html', 
                title = 'Finish')
    return redirect (url_for('surveys.showQuestions',id_survey=id_survey,id_section=section.id))
    # return redirect (url_for('surveys.index'))

@blueprint.route('/survey/<int:id_survey>/consent', methods=['GET', 'POST'])
@login_required
def showConsent(id_survey):
    '''
    Show consent
    '''
    if request.method == 'POST':
        stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)
        stateSurvey.accept_consent()
        return redirect(url_for('surveys.logicSurvey',id_survey = id_survey))
    survey = Survey.query.get(id_survey)
    return render_template('/surveys/consent.html',
        title = survey.title,
        survey = survey,
        consent = survey.consents.first())


def generate_form(questions):
    '''dynamically generates the forms for surveys
    '''
    # def check_answer_expected(id_question):
    #     print "VAMOS ATOMOS", id_question
    #     def _check_answer_expected(self, field):
    #         question = Question.query.get(id_question)
    #         expected_answer = question.expectedAnswer
    #         print "VAMOS ATOMOSsss"
    #         if field.data!=expected_answer:
    #             raise ValidationError("respuesta erronea")
    def check_answer_expected(self,field):
        '''check if the answer is the expected
        '''
        question = Question.query.get(field.name[1:])
        answer = Answer.query.filter(Answer.user_id==g.user.id,
                Answer.question_id==question.id).first()
        if answer is None:
            answer = Answer (answerText = field.data, user= g.user, question = question)
            answer.globalTime = form["globalTimec"+str(question.id)].data
            answer.differentialTime = form["differentialTimec"+str(question.id)].data
        else:
            answer.answerText = field.data
        db.session.add(answer)
        db.session.commit()
        if not answer.answerAttempt():
            if answer.isMoreAttempt():
                raise ValidationError("Wrong answer")
            else:
                flash("wrong answer, you can continue")







    class AnswerForm(Form):
        time = HiddenField('time',default=0)



    for question in questions:

        setattr(AnswerForm,"globalTimec"+str(question.id),HiddenField('globalTimec'+str(question.id),default=0))
        setattr(AnswerForm,"differentialTimec"+str(question.id),HiddenField('differentialTimec'+str(question.id),default=0))

        #added "c" to that the key is valid
        #First element must be a string, otherwise fail to valid choice

        if isinstance (question,QuestionYN):
            if question.required:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = [('Yes','Yes'),('No','No')],validators = [Required()]))
            else:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = [('Yes','Yes'),('No','No')],validators = [Optional()]))
        if isinstance (question,QuestionNumerical):
            if question.required:
                setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))
            else:
                setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'),validators = [Optional()])
        if isinstance (question,QuestionText):
            if question.required:
                if question.regularExpression !="":
                    setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                        validators=[Required(), Regexp(question.regularExpression,0,question.errorMessage)]))
                elif question.isExpectedAnswer():
                    setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Required(),
                        check_answer_expected]))
                elif question.isNumber:
                    setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))
                else:
                    setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Required()]))
            else:
                if question.regularExpression !="":
                    setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                        validators=[Optional(), Regexp(question.regularExpression,0,question.errorMessage)]))
                elif question.isNumber:
                    setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'),validators = [Optional()])
                else:
                    setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Optional()]))
        if isinstance (question,QuestionChoice):
            list = [(str(index),choice) for index, choice in enumerate(question.choices)]
            if question.required:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = list,validators = [Required()]))
            else:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = list,validators = [Optional()]))

        if isinstance (question, QuestionLikertScale):
            list = [(str(index),index) for index in range(question.minLikert,question.maxLikert+1)]
            if question.required:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = list,validators = [Required()]))
            else:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = list,validators = [Optional()]))


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
    return form



@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>', methods=['GET', 'POST'])
@login_required
def showQuestions(id_survey, id_section):
    '''
    Show all question of a section
    '''

    stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user,request.remote_addr)
    section = stateSurvey.nextSection()
    if section is None or section.id !=id_section:
        flash ("access denied")
        raise MyCustom600
        
    survey = Survey.query.get(id_survey)
    section = Section.query.get(id_section)
    questions = section.questions
   
    form = generate_form(questions)

    if form.validate_on_submit():
        for question in questions:
            if isinstance (question,QuestionYN):
                answer = Answer (answerYN = (form["c"+str(question.id)].data=='Yes'), user= g.user, question = question)

            if isinstance (question,QuestionNumerical):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionText):
                answer = Answer (answerText = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionChoice):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question, QuestionLikertScale):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance(question,QuestionPartTwo):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionDecisionOne):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
                answer.globalTime = form["globalTimec"+str(question.id)].data
            if isinstance (question,QuestionDecisionTwo):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionDecisionThree):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionDecisionFour):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)
            if isinstance (question,QuestionDecisionFive):
                answer = Answer (answerYN = (form["c"+str(question.id)].data=='Yes'), user= g.user, question = question)
            if isinstance (question,QuestionDecisionSix):
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= g.user, question = question)

            answer.globalTime = form["globalTimec"+str(question.id)].data
            answer.differentialTime = form["differentialTimec"+str(question.id)].data
            db.session.add(answer)
            db.session.commit()

        stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)
        stateSurvey.finishedSection(form.time.data)
        return redirect(url_for('surveys.logicSurvey',id_survey = id_survey))

    stateSurvey = StateSurvey.getStateSurvey(id_survey,g.user)

    return render_template('/surveys/showQuestions.html',
            title = survey.title,
            survey = survey,
            section = section,
            # form = form,
            form = form,
            questions = questions,
            percent = stateSurvey.percentSurvey()
            )




    


