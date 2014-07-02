from ..models import StateSurvey, Answer, Section, Question, User
from ..models import QuestionYN, QuestionChoice, QuestionText
from ..models import QuestionLikertScale
from app import db, stats_csv
import fcntl
import os
import csv
from app.decorators import async
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import case


@async    
def write_stats(id_survey):

    f1 = open(os.path.join(stats_csv, str(id_survey)+".csv"),"w")
    #lock file
    fcntl.flock(f1, fcntl.LOCK_EX)
    writer = csv.writer(f1, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)
    sequence=[]
    write_header(writer, id_survey,sequence)
    write_answers(writer,id_survey,sequence)

    f1.close()


def write_header(writer,id_survey,sequence):

    def export_section(sections,l,sequence):
    
        def _export_questions(section,l):
            for q in section.questions:
                l.append(q.text)
                l.append("global Time")
                l.append("differential Time")


        for section in sections:
            l.append("Section: \n"+section.title+"\n id:\n"+str(section.id))
            sequence.append(section.id)
            _export_questions(section,l)
            if section.children.count()!=0:
                export_section(section.children,l,sequence)

    l=[]
    l.append("user")
    l.append("ip")
    l.append("start date")
    l.append("finish date")
    l.append("status")
    l.append("sequence")
    sections = Section.query.filter(Section.survey_id==id_survey).order_by(Section.sequence)
    export_section(sections,l,sequence)
    writer.writerow(l)

def write_answers(writer,id_survey,sequence_sections):
    # can not do in a single sql query
    def status(status):
        if status & StateSurvey.FINISH_OK:
            return "finish ok"
        if status & StateSurvey.TIMED_OUT:
            return "out of time"
        if status & StateSurvey.END_DATE_OUT:
            return "out of date"
        return "not finish"


    list_case=[]
    for index,section_id in enumerate(sequence_sections):
        list_case.append((Question.section_id == section_id,index+1))

    questions = Question.query.filter(\
        Question.section_id==Section.id,\
        Section.root_id==id_survey).order_by(\
        case(tuple(list_case)),Question.position)

    answers = Answer.query.filter(\
        User.id==Answer.user_id,\
        Answer.question_id==Question.id,\
        Question.section_id==Section.id,\
        Section.root_id==id_survey).order_by(\
        Answer.user_id,case(tuple(list_case)),Question.position)



    i=0
    len_answers = answers.count()
    len_seq=len(sequence_sections)
    sss=StateSurvey.query.filter(StateSurvey.survey_id==id_survey)

    for ss in sss:
        print ss.user_id
        l=[]
        i_q=0
        i_s=0
        section=sequence_sections[i_s]
        l.append(ss.user_id)
        l.append(ss.ip)
        l.append(ss.start_date)
        l.append(ss.endDate)
        l.append(status(ss.status))
        l.append(ss.sequence)
        l.append(ss.sectionTime.get(section))
        while i<len_answers and answers[i].user_id==ss.user_id and (i_s<len_seq):
            if questions[i_q].section_id!=section:
                l.append(ss.sectionTime.get(section))
                i_s=i_s+1
                section=sequence_sections[i_s]
                print (1)
            else:
                if questions[i_q].id!=answers[i].question_id:
                    print(2)
                    l.append("")
                    l.append("")
                    l.append("")
                    if questions[i_q].isExpectedAnswer():
                        l.append("")
                    i_q=i_q+1
                else:
                    print(3)
                    l.append(answers[i].answerText)
                    l.append(answers[i].globalTime)
                    l.append(answers[i].differentialTime)
                    if answers[i].question.isExpectedAnswer():
                        l.append(answers[i].numberAttempt)
                    i_q=i_q+1
                    i=i+1
        writer.writerow(l)


def write_answers2(writer,id_survey,sequence_sections):
    # can not do in a single sql query
    def status(status):
        if status & StateSurvey.FINISH_OK:
            return "finish ok"
        if status & StateSurvey.TIMED_OUT:
            return "out of time"
        if status & StateSurvey.END_DATE_OUT:
            return "out of date"
        return "not finish"


    list_case=[]
    for index,section_id in enumerate(sequence_sections):
        list_case.append((Question.section_id == section_id,index+1))

    questions = Question.query.filter(\
        Question.section_id==Section.id,\
        Section.root_id==id_survey).order_by(\
        case(tuple(list_case)),Question.position)

    answers = Answer.query.filter(\
        User.id==Answer.user_id,\
        Answer.question_id==Question.id,\
        Question.section_id==Section.id,\
        Section.root_id==id_survey).order_by(\
        Answer.user_id,case(tuple(list_case)),Question.position)



    sss=StateSurvey.query.filter(StateSurvey.survey_id==id_survey)

    for ss in sss:
        l=[]
        anses = answers.filter_by(user_id=ss.user_id)
        j=0
        i_q=0
        section=sequence_sections[j]
        l.append(ss.user_id)
        l.append(ss.ip)
        l.append(ss.start_date)
        l.append(ss.endDate)
        l.append(status(ss.status))
        l.append(ss.sequence)
        l.append(ss.sectionTime.get(section))
        for ans in anses:
            while ans.question.section_id!=section and j<len(sequence_sections):
                l.append(ss.sectionTime.get(section))
                j=j+1
                section=sequence_sections[j]
            if questions[i_q].id!=ans.question_id:
                l.append("")
                l.append("")
                l.append("")
                if questions[i_q].isExpectedAnswer():
                    l.append("")
            else:
                l.append(ans.answerText)
                l.append(ans.globalTime)
                l.append(ans.differentialTime)
                if ans.question.isExpectedAnswer():
                    l.append(ans.numberAttempt)
                i_q=i_q+1
        writer.writerow(l)
