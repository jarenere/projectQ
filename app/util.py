from models import StateSurvey, Answer, Section, Question
import datetime
import random
from app import db, models
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

def matching(survey):
    def match_decision_one():
        pass

    DECISION_ONE=49
    # DEBEN SER PARES!! Y LOS USUARIOS SELECCIONADOS DEL MISMO GRUPO (PAGO Y NO PAGO)
    users = models.User.query.filter(models.User.id==models.StateSurvey.user_id,\
         models.StateSurvey.status==models.StateSurvey.STATUS_FINISH,\
         models.StateSurvey.survey_id==survey.id)
    l=[]
    for i in range(users.count()):
        l.append(users[i].id)
    l_aux=l[:]
    # pop two in two
    for i in range(len(l_aux)/2):
        userA = random.choice(l_aux)
        l_aux.remove(userA)
        userB = random.choice(l_aux)
        l_aux.remove(userB)
        # answerA =db.session.query(models.Answer.id).filter(models.Answer.question_id==49, models.Answer.user_id==2).first()
        answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_ONE).first()
        answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_ONE).first()
        match = models.Match(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            survey=survey.id)
        match.decisionOne()
        db.session.add(match)
    
    l_aux=l[:]
    for i in range(len(l_aux)/2):
        userA = random.choice(l_aux)
        l_aux.remove(userA)
        userB = random.choice(l_aux)
        l_aux.remove(userB)
        answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_ONE).first()
        answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_ONE).first()
        match = models.Match(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            survey=survey.id)
        match.decisionTwo()
        db.session.add(match)
    db.session.commit()

    l_aux=l[:]
    for i in range(len(l_aux)/2):
        userA = random.choice(l_aux)
        l_aux.remove(userA)
        userB = random.choice(l_aux)
        l_aux.remove(userB)
        answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_ONE).first()
        answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_ONE).first()
        match = models.Match(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            survey=survey.id)
        match.decisionThree()
        db.session.add(match)
    db.session.commit()
