from app import db, models
def borrarState():
    state = models.StateSurvey.query.all()
    for s in state:
        db.session.delete(s)
        db.session.commit()

def verAnswers():
    for ans in models.Answer.query.all():
        print ans.id, ans.answerYN, ans.user_id, ans.question_id
        if models.Question.query.get(ans.question_id).type =='partTwo':
          print ans.answerNumeric

def verPreguntas():
    for q in models.Question.query.all():
        print q.id, q.text, q.type
        if q.type =='partTwo':
            for index,i in enumerate(q.choicesPartTwo):
                print "  ", index, i


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