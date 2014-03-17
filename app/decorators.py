from flask.ext.login import current_user
from functools import wraps
from flask import abort
from .models import Section, Survey, Consent, Question



def researcher_required(f):  # pragma: no cover
    """Checks if the user is and researcher or not"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_researcher():
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function


def is_section_researcher(f):
    '''Check if this secction is of the research
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        section = Section.query.get_or_404(kwargs['id_section'])
        survey = Survey.query.get_or_404(kwargs['id_survey'])
        while (section.parent is not None):
            section = section.parent
        if section.survey_id == survey.id and\
            survey.researcher==current_user:
            return f(*args, **kwargs)
        else:
            return abort(403)
    return decorated_function

def belong_researcher(check):
    '''check if section/consent/question/survey belong to researcher
    '''
    def _belong_researcher(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            def check_survey(id_survey):
                survey = Survey.query.get_or_404(id_survey)
                if survey.researcher==current_user:
                    return f(*args, **kwargs)
                else:
                    return abort(403)

            def check_consent(id_survey, id_consent):
                survey = Survey.query.get_or_404(id_survey)
                consent = Consent.query.get_or_404(id_consent)
                if survey.researcher==current_user and\
                    consent.survey_id==survey.id:
                    return f(*args, **kwargs)
                else:
                    return abort(403)

            def check_section(id_survey,id_section):
                section = Section.query.get_or_404(id_section)
                survey = Survey.query.get_or_404(id_survey)
                while (section.parent is not None):
                    section = section.parent
                if section.survey_id == survey.id and\
                    survey.researcher==current_user:
                    return f(*args, **kwargs)
                else:
                    return abort(403)

            def check_question(id_survey,id_section,id_question):
                section = Section.query.get_or_404(id_section)
                survey = Survey.query.get_or_404(id_survey)
                question = Question.query.get_or_404(id_question)
                if question.section!=section:
                    return abort(403)
                while (section.parent is not None):
                    section = section.parent
                if section.survey_id == survey.id and\
                    survey.researcher==current_user:
                    return f(*args, **kwargs)
                else:
                    return abort(403)

            if check == "survey":
                return check_survey(kwargs['id_survey'])
            elif check == "consent":
                return check_consent(kwargs['id_survey'], kwargs['id_consent'])
            elif check == "section":
                return check_section(kwargs['id_survey'], kwargs['id_section'])
            elif check == "question":
                return check_question(kwargs['id_survey'], kwargs['id_section'],kwargs['id_question'])
            else:
                return abort(403)
        return decorated_function
    return _belong_researcher