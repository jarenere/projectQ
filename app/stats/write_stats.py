from ..models import StateSurvey, Answer, Section, Question
from ..models import QuestionYN, QuestionChoice, QuestionNumerical, QuestionText
from ..models import QuestionLikertScale
from app import db, stats_csv
import fcntl
import os
import csv
from app.decorators import async
from sqlalchemy.orm import aliased


@async    
def write_stats(id_user,id_survey):

    f1 = open(os.path.join(stats_csv, str(id_survey)+".csv"),"a+")
    #lock file
    fcntl.flock(f1, fcntl.LOCK_EX)
    writer = csv.writer(f1, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    if os.path.getsize(os.path.join(stats_csv, f1.name))==0:
        write_header(writer, id_survey)
    write_answers(writer,id_survey, id_user)
    #unlock file
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

def write_answers(writer,id_survey, id_user):

    def find_time(list, id):
        find=False
        for i in list:
            if i[0]==id:
                return str(i[1])
                find=True
                break
        if not find:
            return ("None")

    def get_path(sequence,section_time):
        string=""
        for s in sequence:
            string=string+Section.query.get(s).title
            string=string+" :"+find_time(section_time,s)+"\n"
        return string[:-1]


    def get_status(status):
        string=""
        if status & StateSurvey.NONE:
            string = string+"not finished yet\n"
        if status & StateSurvey.FINISH_OK:
            string = string+"finish in time\n"
        if status & StateSurvey.TIMED_OUT:
            string = string+"finished out of time\n"
        if status & StateSurvey.END_DATE_OUT:
            string = string+"finished out of date\n"
        if status & StateSurvey.PART_TWO_MONEY:
            string = string+"part two with money\n"
        if status & StateSurvey.PART_TWO_WITHOUT_MONEY:
            string = string+"part two without money\n"
        if status & StateSurvey.PART_THREE_MONEY:
            string = string+"part three with money\n"
        if status & StateSurvey.PART_THREE_WITHOUT_MONEY:
            string = string+"part three without money\n"
        if status & StateSurvey.MATCHING:
            string = string+"match"
        else:
            string = string+"no match"
        return string


    def _write_answers(section,l):
        stmt1 = db.session.query(Question).\
            filter(Question.section_id==section.id).subquery()
        question1= aliased(Question, stmt1)
        stmt2 = db.session.query(Answer).filter(Answer.user_id==ss.user_id).subquery()
        answer1= aliased(Answer, stmt2)
        res = db.session.query(question1, answer1).\
            outerjoin(answer1, question1.id == answer1.question_id)
        for i in res:
            if i[1] is None:
                l.append("None")
                l.append("None")
                l.append("None")
            else:
                ans = i[1]
                if isinstance (ans.question,QuestionYN):
                    l.append(ans.answerYN)
                if isinstance (ans.question,QuestionText):
                    if ans.question.isNumber:
                        l.append(ans.answerNumeric)
                    else:
                        l.append(ans.answerText)
                if isinstance (ans.question,QuestionChoice):
                    l.append(ans.question.choices[ans.answerNumeric])
                if isinstance (ans.question, QuestionLikertScale):
                    l.append(ans.answerNumeric)
                l.append(ans.globalTime)
                l.append(ans.differentialTime)

    def _export_answers_section(section,l):
            if section.children.count()!=0:
                for s in section.children:
                    l.append(find_time(ss.sectionTime,s.id))
                    _write_answers(s,l)
                    _export_answers_section(s,l)


    ss=StateSurvey.query.filter(StateSurvey.survey_id==id_survey,\
        StateSurvey.user_id==id_user).first()
    if (ss.status & StateSurvey.STATS)==0:  
        ss.status = ss.status | StateSurvey.STATS
        db.session.add(ss)
        db.session.commit()
        l=[]
        l.append(ss.user_id)
        l.append(get_status(ss.status))
        l.append(ss.start_date)
        l.append(ss.endDate)
        l.append(ss.ip)
        l.append(get_path(ss.sequence,ss.sectionTime))
        l.append(ss.sequence)
        sections = Section.query.filter(Section.survey_id==id_survey).order_by(Section.sequence)
        for s in sections:
            l.append(find_time(ss.sectionTime,s.id))
            _export_answers_section(s,l)
        writer.writerow(l)