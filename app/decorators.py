from flask.ext.login import current_user
from functools import wraps
from flask import abort
from main.errors import ErrorEndDateOut
from .models import Section, Survey, Consent, Question, StateSurvey
import datetime
from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper
    


def researcher_required(f):  # pragma: no cover
    """Checks if the user is and researcher or not"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_researcher():
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
                if section.root.id == survey.id and\
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
                if section.root.id == survey.id and\
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


def valid_survey(f):  # pragma: no cover
    '''Checks if the survey is published and the times and the 
        maximum number of users is valid
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        now = datetime.datetime.utcnow()
        survey = Survey.query.get_or_404(kwargs['id_survey'])
        if now > survey.endDate or now < survey.startDate:
            # return abort (404)
            raise ErrorEndDateOut
        return f(*args, **kwargs)
    return decorated_function

def there_is_stateSurvey(f):  # pragma: no cover
    '''Checks if the survey is published and the times and the 
        maximum number of users is valid
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        StateSurvey.query.filter(StateSurvey.survey_id == kwargs['id_survey'], 
            StateSurvey.user_id == current_user.id).first_or_404()
        return f(*args, **kwargs)
    return decorated_function

