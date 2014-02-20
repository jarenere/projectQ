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

