# from ..models import StateSurvey
# from sqlalchemy import and_

# def deleteAnswers():
#     '''Check the time and duration of Survey and 
#     not delete the answers of the surveys that have not
#     been finished
#     '''
#     ss = StateSurvey.query.filter(\
#         and_(StateSurvey.status.op('&')(StateSurvey.FINISH_OK)==0,\
#               StateSurvey.status.op('&')(StateSurvey.FINISH)==0))
#     for s in ss:
#         s.check_survey_duration_and_date()
