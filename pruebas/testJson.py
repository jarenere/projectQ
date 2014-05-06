from app import db, models
from app.models import Section, Survey, Consent
import json

def survey_to_json(survey):
    json_survey = [{
        'title': survey.title,
        'description': survey.description,
        'created': survey.created,
        'startDate': survey.startDate,
        'endDate': survey.endDate,
        'maxNumberRespondents': survey.maxNumberRespondents,
        # 'consents': survey.consents.to_json()
    }]
    return json.dumps(json_survey,indent=2)

def survey_from_json(survey):
    pass

def consent_to_json(consent):
    json_survey = {
            'text': consent.text,
    }
    return json_survey

