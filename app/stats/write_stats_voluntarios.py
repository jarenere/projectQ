from ..models import StateSurvey, Answer, Section, Question
from ..models import QuestionYN, QuestionChoice, QuestionText
from ..models import QuestionLikertScale
from app import db, stats_csv
import fcntl
import os
import csv
from app.decorators import async
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import case


# ans = Answer.query.filter(Answer.user_id==103,Answer.question_id == Question.id, Question.section_id.in_(A)).order_by(sqlalchemy.sql.expression.case(((Answer.section ==6,1),(Answer.section ==5,2),(Answer.section ==7,3))))


# >>> res = db.session.query(question1, answer1).outerjoin(answer1, question1.id == answer1.question_id).order_by(question1.section_id,question1.position)


# >>> res = db.session.query(question1, answer1).outerjoin(answer1, question1.id == answer1.question_id).order_by(sqlalchemy.sql.expression.case(((question1.section_id ==6,1),(question1.section_id ==5,2),(question1.section_id ==7,3),(question1.section_id ==8,4),(question1.section_id ==9,5))))


# write stats of survey "como son nuestos voluntarios" according to the indications of researchers
# identifier blocks the questions of the first part
FIRST_PART=[5,6,7,8,9]
#identifier blocks the questions of the first part
LAST_PART=[14,15]
@async    
def write_stats(id_survey):

    f1 = open(os.path.join(stats_csv, str(id_survey)+".csv"),"w")
    writer = csv.writer(f1, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    write_header(writer, id_survey)
    # for  ss in StateSurvey.query.filter(StateSurvey.survey_id==1,StateSurvey.status.op('&')(StateSurvey.FINISH_OK)):
    #     write_answers(writer, ss.user_id)
    #     print ss.user_id
    # print "done"
    # write_answers2(writer)
    write_answers3(writer)
# MIRAR OUTER JOIN FULL, SOBRE TODO EN COSICAS

    f1.close()


def write_header(writer,id_survey):

    def export_section(id_survey,l):
    
        def _export_questions(section,l):
            for q in section.questions:
                l.append(q.text)
                l.append("global Time")
                l.append("differential Time")

        def _export_section(section,l):
            if section.children.count()!=0:
                for s in section.children:
                    l.append("Section: \n"+s.title+"\n id:\n"+str(s.id))
                    _export_questions(s,l)
                    _export_section(s,l)

        sections = Section.query.filter(Section.survey_id==id_survey).order_by(Section.sequence)
        for s in sections:
            l.append("Section: \n"+s.title+"\n id:\n"+str(s.id))
            _export_questions(s,l)
            _export_section(s,l)


    l=[]
    l.append("user")
    l.append("status")
    l.append("start date")
    l.append("finish date")
    l.append("ip")
    l.append("path")
    export_section(id_survey,l)
    writer.writerow(l)

def write_answers(writer,user_id):

    def _write_answers(l,user_id):
        # probar a hacer una consulta tocha con todo,  y los union, tal vel problema en el order by
        A = [5]
        B = [6,7,8,9,16,17,18,19,46,47,48,58,59,60,49,50,51,61,62,63,32,38,33,39,23,27,14,15]
        
        DECISION1REAL =[40,41,42,43,44,45]
        DECISION1UNREAL=[52,53,54,55,53,57]
        
        PART2 = [16,17,18,19]
        PART3 = [40,41,42,43,44,45,52,53,54,55,56,57,46,47,48,58,59,60,49,50,51,61,62,63,32,38,33,39,23,27]
        FINALPART =[14,15]


        stmt1 = db.session.query(Question).\
            filter(Question.section_id.in_(A)).subquery()
        question1= aliased(Question, stmt1)
        stmt2 = db.session.query(Answer).filter(Answer.user_id==user_id).subquery()
        answer1= aliased(Answer, stmt2)
        # answers a user of block 1 (outerjoin, optional question)
        res1 = db.session.query(question1, answer1).\
            outerjoin(answer1, question1.id == answer1.question_id).order_by(None)
        # answers a user of part2 and some question of part 3(all less decision1), and final part
        res2 = db.session.query(Question, Answer).filter(Answer.user_id==user_id,
            Answer.question_id==Question.id,Question.section_id.in_(B)).order_by(None)

        stmt3 = db.session.query(Question).\
            filter(Question.section_id.in_(DECISION1REAL)).subquery()
        question2= aliased(Question, stmt3)
        # answers a user of decision1, money real (two decision1, only one answer)
        res3 = db.session.query(question2, answer1).\
            outerjoin(answer1, question2.id == answer1.question_id).order_by(None)

        stmt4 = db.session.query(Question).\
            filter(Question.section_id.in_(DECISION1UNREAL)).subquery()
        question3= aliased(Question, stmt4)

        # answers a user of decision1, money untrue (two decision1, only one answer)
        res4 = db.session.query(question3, answer1).\
            outerjoin(answer1, question3.id == answer1.question_id).order_by(None)

        res =res1.union_all(res2,res3,res4).order_by(case((
                (Question.section_id ==5,1),
                (Question.section_id ==6,2),
                (Question.section_id ==7,3),
                (Question.section_id ==8,4),
                (Question.section_id ==9,5),
                (Question.section_id ==16,6),
                (Question.section_id ==17,7),
                (Question.section_id ==18,8),
                (Question.section_id ==19,9),
                (Question.section_id ==40,10),
                (Question.section_id ==41,11),
                (Question.section_id ==42,12),
                (Question.section_id ==43,13),
                (Question.section_id ==44,14),
                (Question.section_id ==45,15),
                (Question.section_id ==52,16),
                (Question.section_id ==53,17),
                (Question.section_id ==54,18),
                (Question.section_id ==55,19),
                (Question.section_id ==56,20),
                (Question.section_id ==57,21),
                (Question.section_id ==46,22),
                (Question.section_id ==47,23),
                (Question.section_id ==48,24),
                (Question.section_id ==58,25),
                (Question.section_id ==59,26),
                (Question.section_id ==60,27),
                (Question.section_id ==49,28),
                (Question.section_id ==50,29),
                (Question.section_id ==51,30),
                (Question.section_id ==61,31),
                (Question.section_id ==62,32),
                (Question.section_id ==63,33),
                (Question.section_id ==32,34),
                (Question.section_id ==38,35),
                (Question.section_id ==33,36),
                (Question.section_id ==39,37),
                (Question.section_id ==23,38),
                (Question.section_id ==27,39),
                (Question.section_id ==14,40),
                (Question.section_id ==15,40))),Question.position)

        for i in res:
            if i[1] is None:
                l.append("None")
                l.append("None")
                l.append("None")
            else:
                ans = i[1]
                l.append(ans.answerText)
                l.append(ans.globalTime)
                l.append(ans.differentialTime)

    l=[]
    _write_answers(l, user_id)
    writer.writerow(l)


def write_answers3(writer):

    def _write_answers(user_id):
        # probar a hacer una consulta tocha con todo,  y los union, tal vel problema en el order by
        A = [5]
        B = [6,7,8,9,16,17,18,19,46,47,48,58,59,60,49,50,51,61,62,63,32,38,33,39,23,27,14,15]
        
        DECISION1REAL =[40,41,42,43,44,45]
        DECISION1UNREAL=[52,53,54,55,53,57]
        
        PART2 = [16,17,18,19]
        PART3 = [40,41,42,43,44,45,52,53,54,55,56,57,46,47,48,58,59,60,49,50,51,61,62,63,32,38,33,39,23,27]
        FINALPART =[14,15]


        stmt1 = db.session.query(Question).\
            filter(Question.section_id.in_(A)).subquery()
        question1= aliased(Question, stmt1)
        stmt2 = db.session.query(Answer).filter(Answer.user_id==user_id).subquery()
        answer1= aliased(Answer, stmt2)
        # answers a user of block 1 (outerjoin, optional question)
        res1 = db.session.query(question1, answer1).\
            outerjoin(answer1, question1.id == answer1.question_id).order_by(None)
        # answers a user of part2 and some question of part 3(all less decision1), and final part
        res2 = db.session.query(Question, Answer).filter(Answer.user_id==user_id,
            Answer.question_id==Question.id,Question.section_id.in_(B)).order_by(None)

        stmt3 = db.session.query(Question).\
            filter(Question.section_id.in_(DECISION1REAL)).subquery()
        question2= aliased(Question, stmt3)
        # answers a user of decision1, money real (two decision1, only one answer)
        res3 = db.session.query(question2, answer1).\
            outerjoin(answer1, question2.id == answer1.question_id).order_by(None)

        stmt4 = db.session.query(Question).\
            filter(Question.section_id.in_(DECISION1UNREAL)).subquery()
        question3= aliased(Question, stmt4)

        # answers a user of decision1, money untrue (two decision1, only one answer)
        res4 = db.session.query(question3, answer1).\
            outerjoin(answer1, question3.id == answer1.question_id).order_by(None)

        res =res1.union_all(res2,res3,res4)

        return res


    l=[]
    for  ss in StateSurvey.query.filter(StateSurvey.survey_id==1,StateSurvey.status.op('&')(StateSurvey.FINISH_OK)):
        l.append(_write_answers(ss.user_id))
        print ss.user_id
    print "done1"

    res = l[0]
    n = 0
    for i in l[1:len(l)]:
        res=res.union_all(i)
        print n
        n= n+1
    print "done2"

    if res is not None:
        user = res[0][1].user_id
    j=[]
    for i in res:
        if i[1].user_id !=user:
            writer.writerow(j)
            user = i[1].user_id
            j=[]
        if i[1] is None:
            j.append("None")
            j.append("None")
            j.append("None")
        else:
            ans = i[1]
            j.append(ans.answerText)
            j.append(ans.globalTime)
            j.append(ans.differentialTime)

    print "done3"


    writer.writerow(j)
    





def write_answers2(writer):
    l=[]
    # probar a hacer una consulta tocha con todo,  y los union, tal vel problema en el order by
    A = [5,6,7,8,9]
    stmt1 = db.session.query(Question).\
        filter(Question.section_id.in_(A)).subquery()
    question1= aliased(Question, stmt1)
    stmt2 = db.session.query(Answer).subquery()
    answer1= aliased(Answer, stmt2)
    res = db.session.query(question1, answer1).\
        outerjoin(answer1, question1.id == answer1.question_id).order_by(
            answer1.user_id,question1.section_id, question1.position)



    B = [16,17,18,19]
    stmt3 = db.session.query(Question).\
        filter(Question.section_id.in_(B)).subquery()
    question2= aliased(Question, stmt3)
    stmt4 = db.session.query(Answer).subquery()
    answer2= aliased(Answer, stmt4)

    res2 = db.session.query(question2, answer2).\
        outerjoin(answer2, question2.id == answer2.question_id).order_by(
            answer2.user_id,question2.section_id, question2.position)

    if res is not None:
        user = res[0][1].user_id

    for i in res:
        if i[1].user_id !=user:
            writer.writerow(l)
            user = i[1].user_id
            l=[]
        if i[1] is None:
            l.append("None")
            l.append("None")
            l.append("None")
        else:
            ans = i[1]
            l.append(ans.answerText)
            l.append(ans.globalTime)
            l.append(ans.differentialTime)


    writer.writerow(l)
    print "done\n"