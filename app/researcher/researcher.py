# -*- coding: utf-8 -*-

from flask import Blueprint, request, url_for, flash, redirect, abort
from flask import render_template
from forms import EditSurveyForm, EditConsentForm, SectionForm
from app.models import Survey, Consent, Section
from app import app, db

blueprint = Blueprint('researcher', __name__)

@blueprint.route('/')
@blueprint.route('/index')
def index():
    surveys = Survey.query.order_by(Survey.created.desc())
    return render_template('/researcher/index.html',
        tittle = 'Survey',
        surveys = surveys)

@blueprint.route('/new', methods = ['GET', 'POST'])
def new():
    form = EditSurveyForm()
    if form.validate_on_submit():
        survey = Survey( title = form.title.data,
            description = form.description.data)
        db.session.add(survey)
        db.session.commit()
        flash('Your survey have been saved.')
        return redirect(url_for('researcher.editSurvey',id = survey.id))
    return render_template('/researcher/new.html',
        title = 'New survey',
        form = form)

@blueprint.route('/edit/<int:id>', methods = ['GET', 'POST'])
#podrimamos definir la entrada como string del titulo+id:
#ejempo: "esto-es-una-encuesta_123", seria mas legible..
#@blueprint.route('/edit/tittle_<int:id>'
def editSurvey(id):
    #get survey
    survey = Survey.query.get(id)
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
    return render_template('/researcher/editSurvey.html',
        title = survey.title,
        form = form,
        survey = survey,
        sections = sections)



@blueprint.route('/edit/<int:id_survey>/consents/', methods = ['GET', 'POST'])
#podrimamos definir la entrada como string del titulo+id:
#ejempo: "esto-es-una-encuesta_123", seria mas legible..
def consents(id_survey):
    form = EditConsentForm()
    survey = Survey.query.get(id_survey)
    if survey == None:
        flash('Survey not found.')
        return redirect(url_for('researcher.index'))
    else:
        consents = survey.consents.all()

    if form.validate_on_submit():
        consent = Consent(text = form.text.data,
            survey_id = id_survey )
        db.session.add(consent)
        db.session.commit()
        flash('Adding consent.')
        return redirect(url_for('researcher.consents',id_survey = survey.id))
 
    return render_template('/researcher/consents.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        consents = consents)

@blueprint.route('/deleteConsent/<int:id_survey>/<int:id_consent>')
def deleteConsent(id_survey,id_consent):
    #>>> cs = models.Consent.query.filter(models.Consent.survey_id == 1, models.Consent.id == 23)
    consent = Consent.query.filter(Consent.survey_id == id_survey, Consent.id == id_consent).first()
    if consent != None:
        #el consentimiento pertence a esa encuesta
        db.session.delete(consent)
        db.session.commit()
        flash('consent removed')
        return redirect(url_for('researcher.consents',id_survey = id_survey))

    else:
        flash('consent wrong') 
        return redirect(url_for('researcher.consents',id_survey = id_survey))


@blueprint.route('/edit/<int:id_survey>/consents/<int:id_consent>', methods = ['GET', 'POST'])
def editConsents(id_survey, id_consent):
    consent = Consent.query.filter(Consent.survey_id == id_survey, Consent.id == id_consent).first()
    if consent == None:
        flash('Consent wrong') 
        return redirect(url_for('researcher.consents',id_survey = id_survey))
    form = EditConsentForm()
    if form.validate_on_submit():
        consent.text = form.text.data
        db.session.add(consent)
        db.session.commit()
        flash('Editing consent')
        return redirect(url_for('researcher.consents',id_survey = id_survey))
    elif request.method != "POST":
        form.text.data = consent.text
        consents = Consent.query.filter(Consent.survey_id == id_survey)
    return render_template('/researcher/consents.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        consents = consents)

@blueprint.route('/survey/<int:id_survey>/section/', methods = ['GET', 'POST'])
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
            survey_id = id_survey )
        db.session.add(section)
        db.session.commit()
        flash('Adding section.')
        return redirect(url_for('researcher.editSurvey',id = survey.id))
    return render_template('/researcher/addSection.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        sections = sections)

@blueprint.route('/edit/<int:id_survey>/section/<int:id_section>', methods = ['GET', 'POST'])
def editSection(id_survey, id_section):
    section = Section.query.filter(Section.survey_id == id_survey, Section.id == id_section).first()
    if section == None:
        flash('Section wrong') 
        return redirect(url_for('researcher.editSurvey',id = id_survey))
    form = SectionForm()
    if form.validate_on_submit():
        section.title = form.title.data
        section.description = form.description.data
        section.sequence = form.sequence.data
        section.percent = form.percent.data
        db.session.add(section)
        db.session.commit()
        flash('Editing consent')
        return redirect(url_for('researcher.editSurvey',id = id_survey))
    elif request.method != "POST":
        form.title.data = section.title
        form.description.data = section.description
        form.sequence.data = section.sequence
        form.percent.data = section.percent
        sections = Section.query.filter(Section.survey_id == id_survey)
    return render_template('/researcher/addSection.html',
        title = "consent",
        form = form,
        id_survey = id_survey,
        sections = sections)