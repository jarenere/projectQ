from models import StateSurvey, Answer, Section, Question
import datetime
from app import db
def check_survey_duration(statusSurvey):
    # return true if duration survey ok, else remove all answers
    now = datetime.datetime.utcnow()
    start = statusSurvey.start_date
    elapsedTime = now - start
    print (statusSurvey.STATUS_NOT_FINISH)
    if elapsedTime.total_seconds()>statusSurvey.survey.duration*60 and \
            statusSurvey.status==StateSurvey.STATUS_NOT_FINISH:
        # time has run out, delete all cuestions
        statusSurvey.status = StateSurvey.STATUS_TIMED_OUT
        db.session.add(statusSurvey)
        db.session.commit()
        # find all answer of user in this survey,
        # I could do a recursive query...
        for s in statusSurvey.sequence:
            section = Section.query.get(s)
            answers = Answer.query.filter(\
                Answer.question_id==Question.id,\
                Question.section_id==section.id,\
                Answer.user_id == statusSurvey.user_id)
            for ans in answers:
                db.session.delete(ans)
        db.session.commit()
        return False
    return True