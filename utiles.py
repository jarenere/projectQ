from app import db, models
def borrarState():
    state = models.StateSurvey.query.all()
    for s in state:
        db.session.delete(s)
    db.session.commit()

def borrarRespeustas():
    for ans in models.Answer.query.all():
        db.session.delete(ans)
    db.session.commit()
    borrarState()

def verAnswers():
    for ans in models.Answer.query.all():
        print ans.id, "user", ans.user.nickname, ans.question_id, ans.question.text
        if ans.question.type=='yn':
            print ans.answerYN
        if ans.question.type =='numerical':
            print ans.answerNumeric
        if ans.question.type== 'text':
            print ans.answerText
        if ans.question.type== 'choice':
            print ans.answerNumeric
        if ans.question.type== 'partTwo':
            print ans.answerNumeric
        if ans.question.type== 'decisionOne':
            print ans.answerNumeric
        if ans.question.type =='decisionTwo':
            print ans.answerNumeric
        if ans.question.type =='decisionThree':
            print ans.answerNumeric
        if ans.question.type =='decisionFour':
            print ans.answerNumeric
        if ans.question.type =='decisionFive':
            print ans.answerYN
        if ans.question.type =='decisionSix':
            print ans.answerNumeric
        print "global:",  ans.globalTime
        print "diferencial:", ans.differentialTime 
        print '================================='

def verPreguntas():
    for q in models.Question.query.all():
        print q.id, q.text, q.type
        if q.type =='partTwo':
            for index,i in enumerate(q.choicesPartTwo):
                print "  ", index, i

def borrarAnswers():
    for ans in models.Answer.query.all():
        db.session.delete(ans)
    db.session.commit()

def generateUserFake(count=100):
    from sqlalchemy.exc import IntegrityError
    from random import seed
    import forgery_py

    seed()
    for i in range(count):
        u = models.User(email=forgery_py.internet.email_address(),
                 nickname=forgery_py.internet.user_name(True))
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def verUsuarios():
    for u in models.User.query.all():
        print u.id, u.email, u.nickname

def generateUserFake1(count=100):
    from sqlalchemy.exc import IntegrityError

    for i in range(count):
        u = models.User(email="user"+str(i)+"gmail.com",
                 nickname="user"+str(i))
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

def verMatching():
    for m in models.Match.query.all():
        print "userA: " , m.userA, "userB: ", m.userB
        print "win: ", m.win
        print "moneyA: ", m.moneyA, "moneyB", m.moneyB
        print "type: ", m.type
        print "__________________"

def borrarMatching():
    ms = models.Match.query.all()
    for m in ms:
        db.session.delete(m)
    db.session.commit()



def generateAnswerFakePart3(id_survey):
    #doy por echo que existen ya lso 100 usuarios de generarUserFake1
    #relleno aleatoriamente uan encuesta con preguntas del tipo decisiones
    import random
    l=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
    l2=[0,2,4,6,8,10,12,14,16,18,20]
    question1 = models.QuestionDecisionOne.query.filter(models.QuestionDecisionOne.section_id==26).first()
    question2 = models.QuestionDecisionTwo.query.filter(models.QuestionDecisionTwo.section_id==27).first()
    question3 = models.QuestionDecisionThree.query.filter(models.QuestionDecisionThree.section_id==28).first()
    question4 = models.QuestionDecisionFour.query.filter(models.QuestionDecisionFour.section_id==29).first()
    questions5 = models.QuestionDecisionFive.query.filter(models.QuestionDecisionFive.section_id==30)
    question6 = models.QuestionDecisionSix.query.filter(models.QuestionDecisionSix.section_id==31).first()

    for i in range(100):
        user = models.User.query.filter(models.User.nickname=="user"+str(i)).first()
        ss =models.StateSurvey.getStateSurvey(id_survey,user,"192.168.0.0")
        ss.status=models.StateSurvey.STATUS_FINISH
        db.session.add(ss)
        answer1=models.Answer(answerNumeric=random.choice(l),user=user,question=question1)
        db.session.add(answer1)
        answer2=models.Answer(answerNumeric=random.choice(l),user=user,question=question2)
        db.session.add(answer2)
        answer3=models.Answer(answerNumeric=random.choice(l),user=user,question=question3)
        db.session.add(answer3)
        answer4=models.Answer(answerNumeric=random.choice(l2),user=user,question=question4)
        db.session.add(answer4)  
        aceptas=random.randrange(0,2)==1
        for q in questions5:
            if not aceptas:
                answer5=models.Answer(answerYN=False,user=user,question=q)
                aceptas=random.randrange(0,2)==1
            else:
                answer5=models.Answer(answerYN=True,user=user,question=q)
            db.session.add(answer5)
        answer6=models.Answer(answerNumeric=random.choice(l2),user=user,question=question6)
        db.session.add(answer6)  


    db.session.commit()

