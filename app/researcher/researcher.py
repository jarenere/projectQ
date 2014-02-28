# -*- coding: utf-8 -*-

from flask import Blueprint, request, url_for, flash, redirect, abort
from flask import render_template
from forms import SurveyForm, EditConsentForm, SectionForm, QuestionForm
from app.models import Survey, Consent, Section
from app.models import Question, QuestionChoice, QuestionNumerical, QuestionText
from app.models import QuestionYN, QuestionLikertScale, QuestionPartTwo, QuestionDecisionOne, \
    QuestionDecisionTwo, QuestionDecisionThree, QuestionDecisionFour, \
    QuestionDecisionFive, QuestionDecisionSix
from app import app, db
from app.decorators import researcher_required
from flask.ext.login import login_user, logout_user, current_user, login_required

blueprint = Blueprint('researcher', __name__)

@blueprint.route('/')
@blueprint.route('/index')
#@login_required
#@researcher_required
def index():
    surveys = Survey.query.order_by(Survey.created.desc())
    return render_template('/researcher/index.html',
        tittle = 'Survey',
        surveys = surveys)

@blueprint.route('/survey/new', methods = ['GET', 'POST'])
def new():
    form = SurveyForm()
    if form.validate_on_submit():
        survey = Survey( title = form.title.data,
            description = form.description.data,
            endDate = form.endDate.data,
            startDate = form.startDate.data)
        db.session.add(survey)
        db.session.commit()
        flash('Your survey have been saved.')
        return redirect(url_for('researcher.editSurvey',id_survey = survey.id))
    return render_template('/researcher/new.html',
        title = 'New survey',
        form = form)



@blueprint.route('/survey/<int:id_survey>', methods = ['GET', 'POST'])
#podrimamos definir la entrada como string del titulo+id:
#ejempo: "esto-es-una-encuesta_123", seria mas legible..
#@blueprint.route('/edit/tittle_<int:id>'
def editSurvey(id_survey):
    #get survey
    survey = Survey.query.get(id_survey)
    sections = survey.sections.all()
    form = SurveyForm()
    if form.validate_on_submit():
        survey.title = form.title.data
        survey.description = form.description.data
        survey.startDate = form.startDate.data
        survey.endDate = form.endDate.data
        db.session.add(survey)
        db.session.commit()
        flash('Your changes have been saved.')
    elif request.method != "POST":
        form.title.data = survey.title
        form.description.data = survey.description
        form.startDate.data = survey.startDate
        form.endDate.data = survey.endDate
    return render_template('/researcher/editSurvey.html',
        title = survey.title,
        form = form,
        survey = survey,
        sections = sections)


@blueprint.route('/edit2/<int:id_survey>', methods = ['GET', 'POST'])
#podrimamos definir la entrada como string del titulo+id:
#ejempo: "esto-es-una-encuesta_123", seria mas legible..
#@blueprint.route('/edit/tittle_<int:id>'
def editSurvey2(id_survey):
    #get survey
    survey = Survey.query.get(id_survey)
    #survey = Survey.query.filter(Survey.id == id)
    sections = survey.sections.all()
    form = EditSurveyForm()
    if form.validate_on_submit():
        survey.title = form.title.data
        survey.description = form.description.data
        db.session.add(survey)
        db.session.commit()
        flash('Your changes have been saved.')
    elif request.method != "POST":
        form.title.data = survey.title
        form.description.data = survey.description
    return render_template('/researcher/editSurvey2.html',
        title = survey.title,
        form = form,
        survey = survey,
        sections = sections)


@blueprint.route('/survey/<int:id_survey>/consent/add', methods = ['GET', 'POST'])
#podrimamos definir la entrada como string del titulo+id:
#ejempo: "esto-es-una-encuesta_123", seria mas legible..
def addConsent(id_survey):
    form = EditConsentForm()
    survey = Survey.query.get(id_survey)
    if survey == None:
        flash('Survey not found.')
        return redirect(url_for('researcher.index'))
    else:
        consents = survey.consents.all()

    if form.validate_on_submit():
        consent = Consent(text = form.text.data,
            survey = survey)
        db.session.add(consent)
        db.session.commit()
        flash('Adding consent.')
        return redirect(url_for('researcher.addConsent',id_survey = survey.id))
 
    return render_template('/researcher/consents.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        consents = consents,
        addConsent = True)

@blueprint.route('/survey/<int:id_survey>/consent/<int:id_consent>/delete')
def deleteConsent(id_survey,id_consent):
    consent = Consent.query.filter(Consent.survey_id == id_survey, Consent.id == id_consent).first()
    if consent != None:
        db.session.delete(consent)
        db.session.commit()
        flash('consent removed')
        return redirect(url_for('researcher.addConsent',id_survey = id_survey))
    else:
        flash('consent wrong') 
        return redirect(url_for('researcher.addConsent',id_survey = id_survey))


@blueprint.route('/survey/<int:id_survey>/consent/<int:id_consent>', methods = ['GET', 'POST'])
def editConsents(id_survey, id_consent):
    consent = Consent.query.filter(Consent.survey_id == id_survey, Consent.id == id_consent).first()
    if consent == None:
        flash('Consent wrong') 
        return redirect(url_for('researcher.addConsent',id_survey = id_survey))
    form = EditConsentForm()
    if form.validate_on_submit():
        consent.text = form.text.data
        db.session.add(consent)
        db.session.commit()
        flash('Edited consent')
        return redirect(url_for('researcher.addConsent',id_survey = id_survey))
    elif request.method != "POST":
        form.text.data = consent.text
        consents = Consent.query.filter(Consent.survey_id == id_survey)
    return render_template('/researcher/consents.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        consents = consents,
        editConsent = True)

@blueprint.route('/survey/<int:id_survey>/section/new', methods = ['GET', 'POST'])
def addSection(id_survey):
    form = SectionForm()
    survey = Survey.query.get(id_survey)
    if survey == None:
        flash('Survey not found.')
        return redirect(url_for('researcher.index'))
    else:
        sections = survey.sections.all()
    if form.validate_on_submit():
        section = Section(title = form.title.data,
            description = form.description.data,
            sequence = form.sequence.data,
            percent = form.percent.data,
            survey = survey
            )
        db.session.add(section)
        db.session.commit()
        flash('Adding section.')
        return redirect(url_for('researcher.editSurvey',id_survey = survey.id))
    return render_template('/researcher/addEditSection.html',
        title = "consent",
        form = form,
        survey = survey,
        sections = sections,
        #add = true, you is adding a new section
        addSection = True)

@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>', methods = ['GET', 'POST'])
def editSection(id_survey, id_section):
    section = Section.query.get(id_section)
    if section == None:
        flash('Section wrong') 
        return redirect(url_for('researcher.editSurvey',id_survey = id_survey))
    form = SectionForm()
    sections = Survey.query.get(id_survey).sections.all()
    if form.validate_on_submit():
        section.title = form.title.data
        section.description = form.description.data
        section.sequence = form.sequence.data
        section.percent = form.percent.data
        db.session.add(section)
        db.session.commit()
        flash('Save changes')
        return redirect(url_for('researcher.editSection',id_survey = id_survey, id_section = id_section))
    elif request.method != "POST":
        form.title.data = section.title
        form.description.data = section.description
        form.sequence.data = section.sequence
        form.percent.data = section.percent
    return render_template('/researcher/addEditSection.html',
        title = "consent",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = sections,
        #add = true, you is adding a new section, add = False you is editing a section
        editSection = True,
        id_section = id_section)

@blueprint.route('/survey/<int:id_survey>/deleteSection/<int:id_section>')
def deleteSection(id_survey,id_section):
        #
        #CUANDO TENGA SUBSECCIONES Y ENCUESTAR, EL ELIMINAR NO ES TRIVIAL
        #
    section = Section.query.get(id_section)
    if section != None:
        #el consentimiento pertence a esa encuesta
        db.session.delete(section)
        db.session.commit()
        flash('Section removed')
        return redirect(url_for('researcher.editSurvey',id_survey = id_survey))
    else:
        flash('Section wrong') 
        return redirect(url_for('researcher.editSurvey',id_survey = id_survey))

@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/new', methods = ['GET', 'POST'])
def addSubSection(id_survey, id_section):
    parentSection = Section.query.get(id_section)
    if parentSection == None:
        flash('Section wrong') 
        return redirect(url_for('researcher.editSection',id_survey = id_survey, id_section = id_section))
    form = SectionForm()
    if form.validate_on_submit():
        section = Section(title = form.title.data,
            description = form.description.data,
            sequence = form.sequence.data,
            percent = form.percent.data,
            parent = parentSection)
        db.session.add(section)
        db.session.commit()
        flash('Adding subsection.')
        return redirect(url_for('researcher.editSection',id_survey = id_survey, id_section = id_section))
    return render_template('/researcher/addEditSection.html',
        title = "consent",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        addSubSection = True)


def selectType(form):

    if form.questionType.data =='YES/NO':
        question = QuestionYN()
    if form.questionType.data == 'Numerical':
        question = QuestionNumerical()
    if form.questionType.data == 'Text':
        question = QuestionText()
    if form.questionType.data == 'Choice':
        l = [form.answer1.data,
        form.answer2.data,
        form.answer3.data,
        form.answer4.data,
        form.answer5.data,
        form.answer6.data,
        form.answer7.data,
        form.answer8.data,
        form.answer9.data]
        question = QuestionChoice(choices = l[0:int(form.numberFields.data)])
    if form.questionType.data == 'likert':
        question = QuestionLikertScale(minLikert=form.minLikert.data,
            maxLikert=form.maxLikert.data, labelMin=form.labelMinLikert.data,
            labelMax=form.labelMaxLikert.data)
    if form.questionType.data == 'PartTwo':
        l = [form.answer1.data,
        form.answer2.data]
        question = QuestionPartTwo(choices = l[0:2])
    if form.questionType.data == 'DecisionOne':
        question = QuestionDecisionOne()
    if form.questionType.data == 'DecisionTwo':
        question = QuestionDecisionTwo()
    if form.questionType.data == 'DecisionThree':
        question = QuestionDecisionThree()
    if form.questionType.data == 'DecisionFour':
        question = QuestionDecisionFour()
    if form.questionType.data == 'DecisionFive':
        l = [form.answer1.data]
        question = QuestionDecisionFive(choices = l[0:1])
    if form.questionType.data == 'DecisionSix':
        question = QuestionDecisionSix()
           
    question.text = form.text.data
    question.required = form.required.data
    question.registerTime = form.registerTime.data
    question.expectedAnswer = form.expectedAnswer.data
    question.numberAttempt = form.numberAttempt.data
    return question


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/addQuestion', methods = ['GET', 'POST'])
def addQuestion(id_survey, id_section):
    section = Section.query.get(id_section)
    if section == None:
        flash('Section wrong') 
        return redirect(url_for('researcher.editSection',id_survey = id_survey, id_section = id_section))
    form = QuestionForm()
    
    if form.validate_on_submit():
        question = selectType(form)

        question.section = section
        db.session.add(question)
        db.session.commit()
        flash('Adding question')
        return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section = id_section))
    
    return render_template('/researcher/addEditQuestion.html',
        title = "Question",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        section = section,
        questions = section.questions)

@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/question/<int:id_question>', methods = ['GET', 'POST'])
def editQuestion(id_survey, id_section,id_question):
    question = Question.query.get(id_question)
    if question == None:
        flash('Question wrong') 
        return redirect(url_for('researcher.editSection',id_survey = id_survey, id_section = id_section))
    form = QuestionForm()    
    if form.validate_on_submit():
        q = selectType(form)
        q.id = question.id
        q.section = question.section
        db.session.delete (question)
        db.session.commit()
        db.session.add(q)
        db.session.commit()
        flash('Adding question')
        return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section = id_section))
    elif request.method != "POST":
        form.text.data = question.text
        form.required.data = question.required
        form.registerTime.data = question.registerTime
        form.expectedAnswer.data = question.expectedAnswer
        form.numberAttempt.data = question.numberAttempt
        if isinstance (question,QuestionChoice):
            l= question.choices
            if len(l) >0:
                form.answer1.data = l[0]
            if len(l) >1:
                form.answer2.data = l[1]
            if len(l) >2:
                form.answer3.data = l[2]
            if len(l) >3:
                form.answer4.data = l[3]
            if len(l) >4:
                form.answer5.data = l[4]
            if len(l) >5:
                form.answer6.data = l[5]
            if len(l) >6:
                form.answer7.data = l[6]
            if len(l) >7:
                form.answer8.data = l[7]
            if len(l) >8:
                form.answer9.data = l[8]
        if isinstance (question,QuestionPartTwo):
            l= question.choices
            form.answer1.data = l[0]
            form.answer2.data = l[1]
        if isinstance (question,QuestionDecisionFive):
            l= question.choices
            form.answer1.data = l[0]
        if isinstance(question, QuestionLikertScale):
            form.labelMinLikert.data=question.labelMin
            form.labelMaxLikert.data=question.labelMax

    return render_template('/researcher/addEditQuestion.html',
        title = "Question",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        section = Section.query.get(id_section),
        questions = Section.query.get(id_section).questions)

@blueprint.route('/survey/<int:id_survey>/Section/<int:id_section>/deleteQuestion/<int:id_question>')
def deleteQuestion(id_survey,id_section,id_question):
        #
        #CUANDO TENGA SUBSECCIONES Y ENCUESTAR, EL ELIMINAR NO ES TRIVIAL
        #
    question = Question.query.get(id_question)
    if question != None:
        #el consentimiento pertence a esa encuesta
        db.session.delete(question)
        db.session.commit()
        flash('Question removed')
        return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section=id_section))
    else:
        flash('Question wrong') 
        return redirect(url_for('researcher.editSurvey',id_survey = id_survey))