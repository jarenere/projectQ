from app.models import  QuestionChoice, QuestionYN, QuestionText, QuestionLikertScale
from app.models import Answer


def generate_answer(question,form,user):
    answer = Answer.query.filter(Answer.user_id==user.id,
            Answer.question_id==question.id).first()
    if answer is None:
        return new_answer(question,form,user)
    else:
        return update_answer(question, form, user, answer)


def new_answer(question,form,user):
    if isinstance (question,QuestionYN):
        answer = Answer (answerYN = (form["c"+str(question.id)].data=='Yes'), user= user, question = question)
        answer.answerText = str(answer.answerYN)
    if isinstance (question,QuestionText):
        if question.isNumber:
            if question.isNumberFloat:
                answer = Answer (answerNumeric = form["c"+str(question.id)].data.replace(",","."), user= user, question = question)
            else:
                answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= user, question = question)
            answer.answerText= answer.answerNumeric
        else:
            answer = Answer (answerText = form["c"+str(question.id)].data, user= user, question = question)
    if isinstance (question,QuestionChoice):
        answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= user, question = question)
        answer.answerText = form["c"+str(question.id)].choices[int(form["c"+str(question.id)].data)][1]
    if isinstance (question, QuestionLikertScale):
        answer = Answer (answerNumeric = form["c"+str(question.id)].data, user= user, question = question)
        answer.answerText = form["c"+str(question.id)].choices[int(form["c"+str(question.id)].data)][1]
    answer.globalTime = form["globalTimec"+str(question.id)].data
    answer.differentialTime = form["differentialTimec"+str(question.id)].data
    return answer

def update_answer(question,form,user,answer):
    if isinstance(question,QuestionText):
        if question.isNumber:
            answer.answerNumeric = form["c"+str(question.id)].data.replace(",",".")
            answer.answerText= answer.answerNumeric
        else:
            answer.answerText = form["c"+str(question.id)].data
    elif isinstance(question,QuestionYN):
        answer.answerYN = form["c"+str(question.id)].data=='Yes'
        answer.answerText = str(answer.answerYN)
    elif isinstance(question,QuestionChoice) or isinstance(question,QuestionLikertScale):
        answer.answerNumeric = form["c"+str(question.id)].data
        answer.answerText = form["c"+str(question.id)].choices[int(form["c"+str(question.id)].data)][1]
    answer.globalTime = form["globalTimec"+str(question.id)].data
    answer.differentialTime = form["differentialTimec"+str(question.id)].data
    return answer