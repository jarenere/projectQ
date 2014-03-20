from app.models import StateSurvey, Answer, Section, Question
import datetime
import random
from app import db, models

def matching(survey):
    def generate_tupla(list_users):
        '''can succes-> l[i][0]==l[i][1]
        '''
        l_aux1=list_users[:]
        l_aux2=list_users[:]
        l=[]
        for i in range(len(list_users)):
            userA = random.choice(l_aux1)
            userB = random.choice(l_aux2)
            l_aux1.remove(userA)
            l_aux2.remove(userB)
            l.append((userA,userB))
        return l
    def match_decision_one(list_users):

        # pop two in two
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            # answerA =db.session.query(models.Answer.id).filter(models.Answer.question_id==49, models.Answer.user_id==2).first()
            answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_ONE).first()
            answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_ONE).first()
            match = models.Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionOne()
            db.session.add(match)

    def match_decision_two(list_users):
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_TWO).first()
            answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_TWO).first()
            match = models.Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionTwo()
            db.session.add(match)

    def match_decision_three(list_users):
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            answerA = models.Answer.query.filter_by(user_id=userA,question_id=DECISION_THREE).first()
            answerB = models.Answer.query.filter_by(user_id=userB,question_id=DECISION_THREE).first()
            match = models.Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionThree()
            db.session.add(match)

    def match_decision_four(list_users):

        l=generate_tupla(list_users)
        for i in range(len(l)):
            answerA = models.Answer.query.filter_by(user_id=l[i][0],question_id=DECISION_FOUR).first()
            match = models.Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=survey.id)
            match.decisionFour(SECTION_DECISION_FIVE)
            db.session.add(match)

    def match_decision_six(list_users):

        l=generate_tupla(list_users)
        for i in range(len(l)):
            answerA = models.Answer.query.filter_by(user_id=l[i][0],question_id=DECISION_SIX).first()
            match = models.Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=survey.id)
            match.decision_six()
            db.session.add(match)


    DECISION_ONE=47
    DECISION_TWO=48
    DECISION_THREE=49
    DECISION_FOUR=50
    SECTION_DECISION_FIVE=27
    DECISION_SIX=62
    # DEBEN SER PARES!! Y LOS USUARIOS SELECCIONADOS DEL MISMO GRUPO (PAGO Y NO PAGO)
    # users = models.User.query.filter(models.User.id==models.StateSurvey.user_id,\
    #      models.StateSurvey.status==models.StateSurvey.FINISH,\
    #      models.StateSurvey.survey_id==survey.id)
    state_surveys = models.StateSurvey.query.filter(models.User.id==models.StateSurvey.user_id,\
         models.StateSurvey.status==models.StateSurvey.FINISH_OK | models.StateSurvey.FINISH,\
         models.StateSurvey.survey_id==survey.id)

    l=[]
    if state_surveys.count()%2 == 0:
        for i in range(state_surveys.count()):
            l.append(state_surveys[i].user_id)
            state_surveys[i].status=state_surveys[i].status & models.StateSurvey.MATCHING
            db.session.add(state_surveys[i])
    else:
        # impar, last user out!
        for i in range(state_surveys.count()-1):
            l.append(state_surveys[i].user_id)
            state_surveys[i].status=state_surveys[i].status & models.StateSurvey.MATCHING
            db.session.add(state_surveys[i])

    
    l_aux=l[:]
    match_decision_one(l_aux)

    l_aux=l[:]
    match_decision_two(l_aux)

    l_aux=l[:]
    match_decision_three(l_aux)

    l_aux=l[:]
    match_decision_four(l_aux)

    l_aux=l[:]
    match_decision_six(l_aux)

    db.session.commit()
