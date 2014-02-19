from app import db, models
def borrarState():
    state = models.StateSurvey.query.all()
    for s in state:
        db.session.delete(s)
        db.session.commit()

def verAnswers():
    for ans in models.Answer.query.all():
        print ans.id, ans.answerYN, ans.user_id, ans.question_id