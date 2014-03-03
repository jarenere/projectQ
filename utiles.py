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

def verMatch():
    for m in models.Match.query.all():
        print m.id