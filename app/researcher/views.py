# -*- coding: utf-8 -*-

from flask import Blueprint, request, url_for, flash, redirect, abort, send_file
from flask import render_template, g, current_app
from forms import SurveyForm, EditConsentForm, SectionForm, QuestionForm
from app.models import Survey, Consent, Section, StateSurvey, Answer
from app.models import Question, QuestionChoice, QuestionText
from app.models import QuestionYN, QuestionLikertScale
from app.models import Condition
from app import db
from app.decorators import researcher_required, belong_researcher
from flask.ext.login import login_user, logout_user, current_user, login_required
import tempfile
from werkzeug import secure_filename
from . import blueprint
from sqlalchemy.orm import aliased
import csv


@blueprint.route('/')
@blueprint.route('/index')
@login_required
@researcher_required
def index():
    surveys = Survey.query.filter(Survey.researcher==g.user).order_by(Survey.created.desc())
    return render_template('/researcher/index.html',
        tittle = 'Survey',
        surveys = surveys)


@blueprint.route('/survey/new', methods = ['GET', 'POST'])
@login_required
@researcher_required
def new():
    form = SurveyForm()
    if form.validate_on_submit():
        # file = request.files['file']
        # if file:
        filename = secure_filename(form.surveyXml.data.filename)
        if filename:
            tf = tempfile.NamedTemporaryFile()
            form.surveyXml.data.save(tf.name)
            msg, survey = Survey.from_xml(tf.name, g.user)
            tf.close()
            for m in msg:
                flash(m)
            return redirect(url_for('researcher.index'))
        else:
            survey = Survey( title = form.title.data,
                description = form.description.data,
                endDate = form.endDate.data,
                startDate = None,
                maxNumberRespondents = form.maxNumberRespondents.data,
                duration = form.duration.data,
                researcher = g.user)
            db.session.add(survey)
            db.session.commit()
            flash('Your survey have been saved.')
        return redirect(url_for('researcher.editSurvey',id_survey = survey.id))
    return render_template('/researcher/new.html',
        title = 'New survey',
        form = form)


@blueprint.route('/survey/<int:id_survey>', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('survey')
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
        survey.maxNumberRespondents = form.maxNumberRespondents.data
        survey.duration = form.duration.data
        db.session.add(survey)
        db.session.commit()
        flash('Your changes have been saved.')
    elif request.method != "POST":
        form.title.data = survey.title
        form.description.data = survey.description
        form.startDate.data = survey.startDate
        form.endDate.data = survey.endDate
        form.maxNumberRespondents.data = survey.maxNumberRespondents
        form.duration.data = survey.duration
    return render_template('/researcher/editSurvey.html',
        title = survey.title,
        form = form,
        survey = survey,
        sections = sections)


@blueprint.route('/survey/deleteSurvey/<int:id_survey>')
@login_required
@researcher_required
@belong_researcher('survey')
def deleteSurvey(id_survey):
    survey = Survey.query.get(id_survey)
    db.session.delete(survey)
    db.session.commit()
    flash('Survey removed')
    return redirect(url_for('researcher.index'))


@blueprint.route('/survey/exportSurvey/<int:id_survey>')
@login_required
@researcher_required
@belong_researcher('survey')
def exportSurvey(id_survey):
    '''http://stackoverflow.com/questions/14614756/how-can-i-generate-file-on-the-fly-and-delete-it-after-download
        http://stackoverflow.com/questions/13344538/how-to-clean-up-temporary-file-used-with-send-file/
    '''
    survey = Survey.query.get(id_survey)
    xml = survey.to_xml()
    tf = tempfile.NamedTemporaryFile()
    xml.write(tf.name,encoding="ISO-8859-1", method="xml")
    flash('Survey exported')
    return send_file(tf, as_attachment=True, attachment_filename=survey.title+'.xml')

def tips_path(section=None):
    '''Return a list with the path of a section
    '''
    l=[]
    if section is not None:
        l.append((section.title, section.id))
        while (section.parent is not None):
            l.append((section.parent.title, section.parent.id))
            section = section.parent
    l.reverse()
    return l


@blueprint.route('/survey/<int:id_survey>/consent/add', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('survey')
def addConsent(id_survey):
    form = EditConsentForm()
    survey = Survey.query.get(id_survey)
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
@login_required
@researcher_required
@belong_researcher('consent')
def deleteConsent(id_survey,id_consent):
    consent = Consent.query.get(id_consent)
    db.session.delete(consent)
    db.session.commit()
    flash('consent removed')
    return redirect(url_for('researcher.addConsent',id_survey = id_survey))


@blueprint.route('/survey/<int:id_survey>/consent/<int:id_consent>', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('consent')
def editConsents(id_survey, id_consent):
    consent = Consent.query.get(id_consent)
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
@login_required
@researcher_required
@belong_researcher('survey')
def addSection(id_survey):
    survey = Survey.query.get(id_survey)
    form = SectionForm()
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
    # heuristics of the next sequence
    section = Section.query.filter(Section.survey_id==id_survey).order_by(Section.sequence.desc())
    if section.count()>=2 and section[0].sequence==section[1].sequence:
        # see the last and  penultimate
        form.sequence.data= section[0].sequence
    elif section.count()>=1:
        form.sequence.data= section[0].sequence + 1
    else:
        form.sequence.data =1
    return render_template('/researcher/addEditSection.html',
        title = "Section",
        form = form,
        survey = survey,
        sections = survey.sections.all(),
        #add = true, you is adding a new section
        addSection = True)


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('section')
def editSection(id_survey, id_section):
    section = Section.query.get(id_section)
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
    path=tips_path(section)
    return render_template('/researcher/addEditSection.html',
        title = "Section",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = sections,
        editSection = True,
        id_section = id_section,
        path = path)


@blueprint.route('/survey/<int:id_survey>/deleteSection/<int:id_section>')
@login_required
@researcher_required
@belong_researcher('section')
def deleteSection(id_survey,id_section):
    section = Section.query.get(id_section)
    db.session.delete(section)
    db.session.commit()
    flash('Section removed')
    return redirect(url_for('researcher.editSurvey',id_survey = id_survey))


@blueprint.route('/survey/<int:id_survey>/duplicateSection/<int:id_section>')
@login_required
@researcher_required
@belong_researcher('section')
def duplicate_section(id_survey,id_section):
    section = Section.query.get(id_section)
    section.duplicate()
    flash('Section duplicated')
    return redirect(url_for('researcher.editSurvey',id_survey = id_survey))


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/new', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('section')
def addSubSection(id_survey, id_section):
    parentSection = Section.query.get(id_section)
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
    # heuristics of the next sequence
    section = Section.query.filter(Section.parent_id==id_section).order_by(Section.sequence.desc())
    if section.count()>=2 and section[0].sequence==section[1].sequence:
        # see the last and  penultimate
        form.sequence.data= section[0].sequence
    elif section.count()>=1:
        form.sequence.data= section[0].sequence + 1
    else:
        form.sequence.data =1
    path=tips_path(parentSection)
    return render_template('/researcher/addEditSection.html',
        title = "Section",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        addSubSection = True,
        path = path)


def selectType(form,section):
    '''Function that read the form and generates the object the type Question 
    '''
    if form.questionType.data =='yn':
        question = QuestionYN()
    if form.questionType.data == 'text':
        question = QuestionText(isNumber=form.isNumber.data,
            isNumberFloat=form.isNumberFloat.data,
            regularExpression=form.regularExpression.data,
            errorMessage=form.errorMessage.data)
    if form.questionType.data == 'choice':
        if form.range_min.data is not None:
            question = QuestionChoice(range_min=form.range_min.data,
                range_max=form.range_max.data,
                range_step = form.range_step.data)
        else:
            l = [form.answer1.data,
            form.answer2.data,
            form.answer3.data,
            form.answer4.data,
            form.answer5.data,
            form.answer6.data,
            form.answer7.data,
            form.answer8.data,
            form.answer9.data,
            form.answer10.data,
            form.answer11.data,
            form.answer12.data]
            l_aux=[]
            for i in l:
                if len(i)!=0:
                    l_aux.append(i)    
            question = QuestionChoice(choices = l_aux)
        question.render = form.render.data
    if form.questionType.data == 'likertScale':
        question = QuestionLikertScale(minLikert=form.minLikert.data,
            maxLikert=form.maxLikert.data, labelMin=form.labelMinLikert.data,
            labelMax=form.labelMaxLikert.data)
    # subquestion
    if form.operation.data!='none':
        condition=Condition(operation=form.operation.data,
            value=form.value.data)
        db.session.add(condition)
        question.condition=condition
        question.parent=form.question.data

    #decision:
    if form.decisionType.data !='none':
        question.is_real_money= form.is_real_money.data
    if form.decisionType.data == "part_two":
        l = [form.answer1.data,
        form.answer2.data]
        question.choices = l[0:2]
    if form.decisionType.data == "decision_five":
        l = [form.container.data]
        question.container = l[0:1]


    if form.feedback.data:
        question.container = ["feedback"]

    question.decision=form.decisionType.data
    question.text = form.text.data
    question.required = form.required.data
    question.expectedAnswer = form.expectedAnswer.data
    question.maxNumberAttempt = form.maxNumberAttempt.data
    question.section=section
    question.last_position()
    return question


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/addQuestion', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('section')
def addQuestion(id_survey, id_section):
    section = Section.query.get(id_section)
    form = QuestionForm()
    # get list of question of this section, to that question depends on the answer to another question
    form.question.query=Question.query.filter(Question.section_id==id_section)
    if form.validate_on_submit():
        question = selectType(form,section)
        db.session.add(question)
        db.session.commit()
        flash('Adding question')
        return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section = id_section))
    path=tips_path(section)
    return render_template('/researcher/addEditQuestion.html',
        title = "Question",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        section = section,
        questions = section.questions,
        addQuestion = True,
        question_type = form.questionType.data,
        decision_type = form.decisionType.data,
        operation = form.operation.data,
        path = path)


@blueprint.route('/survey/<int:id_survey>/section/<int:id_section>/question/<int:id_question>', methods = ['GET', 'POST'])
@login_required
@researcher_required
@belong_researcher('question')
def editQuestion(id_survey, id_section,id_question):
    question = Question.query.get(id_question)
    form = QuestionForm()
    # get list of question of this section, to that question depends on the answer to another question
    form.question.query=Question.query.filter(Question.section_id==id_section,\
        Question.id!=id_question)
    if form.validate_on_submit():
        q = selectType(form,Section.query.get(id_section))
        for subquestion in question.subquestions:
            subquestion.parent = q
            db.session.add(subquestion)
        q.position=question.position
        db.session.add(q)
        db.session.commit()
        db.session.delete (question)
        db.session.commit()
        db.session.commit()
        flash('Adding question')
        return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section = id_section))
    elif request.method != "POST":
        form.text.data = question.text
        form.required.data = question.required
        form.expectedAnswer.data = question.expectedAnswer
        form.maxNumberAttempt.data = question.maxNumberAttempt
        form.is_real_money.data = question.is_real_money
        if isinstance(question, QuestionText):
            form.regularExpression.data = question.regularExpression
            form.isNumber.data = question.isNumber
            form.isNumberFloat.data = question.isNumberFloat
            form.errorMessage.data = question.errorMessage
        if isinstance (question,QuestionChoice):
            if question.is_range:
                form.range_min.data = question.range_min
                form.range_max.data = question.range_max
                form.range_step.data = question.range_step
            else:
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
                if len(l) >9:
                    form.answer10.data = l[9]
                if len(l) >10:
                    form.answer11.data = l[10]
                if len(l) >11:
                    form.answer12.data = l[11]
        if isinstance(question, QuestionLikertScale):
            form.labelMinLikert.data=question.labelMin
            form.labelMaxLikert.data=question.labelMax
        if question.decision=="decision_five":
            form.container.data = question.container[0] if len(question.container)>0 else 0
        
        if question.container is not None:
            if len(question.container)>0 and question.container[0]=="feedback":
                form.feedback.data=True

        # condition of subquestion
        if question.condition is not None:
            form.value.data =question.condition.value

    section =  Section.query.get(id_section)
    path=tips_path(section)
    return render_template('/researcher/addEditQuestion.html',
        title = "Question",
        form = form,
        survey = Survey.query.get(id_survey),
        sections = Survey.query.get(id_survey).sections.all(),
        section = section,
        questions = Section.query.get(id_section).questions,
        editQuestion = True,
        question_type = question.type,
        decision_type = question.decision,
        render = question.render if isinstance(question,QuestionChoice) else "vertical",
        operation = (form.operation.data if question.condition is None else\
            question.condition.operation),
        question = (None if question.parent is None else question.parent_id),
        path = path)


@blueprint.route('/survey/<int:id_survey>/Section/<int:id_section>/deleteQuestion/<int:id_question>')
@login_required
@researcher_required
@belong_researcher('question')
def deleteQuestion(id_survey,id_section,id_question):
        #
        #CUANDO TENGA SUBSECCIONES Y ENCUESTAR, EL ELIMINAR NO ES TRIVIAL
        #
    question = Question.query.get(id_question)
    db.session.delete(question)
    db.session.commit()
    flash('Question removed')
    return redirect(url_for('researcher.addQuestion',id_survey = id_survey, id_section=id_section))


@blueprint.route('/survey/exportStats/<int:id_survey>')
@login_required
@researcher_required
@belong_researcher('survey')
def export_stats(id_survey):
    '''Export stats in csv
    '''

    # survey = Survey.query.get(id_survey)
    # #ofile = tempfile.NamedTemporaryFile()
    # ofile  = open('test.csv', "wb")
    # writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    # # export_users(writer)
    # # export_section(writer)
    # # export_section_user(writer)
    # # export_section_question(writer)
    # # export_question_user(writer)
    # # l=["jaja"]
    # # writer.writerow(l)
    # # export_questions(writer,id_survey)
    # write_header(writer,id_survey)
    # write_answers(writer,id_survey)
    # ofile.close()
    # flash ("Export stats")
    #return send_file(ofile, as_attachment=True, attachment_filename="stats_"+survey.title+'.csv')
    if current_app.config.get('MODE_GAMES',False):
        from app.stats.write_stats_voluntarios import write_stats
        write_stats(id_survey)
    else:
        from app.stats.write_stats import write_stats
        write_stats(id_survey) 
        
    return redirect(url_for('researcher.index'))