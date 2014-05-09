import unittest
from flask import  g, flash
from app import app,db
from app.models import User,ROLE_RESEARCHER
from app.models import Survey, Section
from app.models import QuestionText,QuestionChoice,QuestionYN
from app.models import Condition
from app.surveys.forms import CheckAnswerExpected, CheckSubquestion, RequiredSelectField
from app.surveys.forms import generate_form
import os
from config import basedir
from wtforms import ValidationError
from wtforms.validators import StopValidation


class ValidatorTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_check_answer_expected(self):
        u1 = User(nickname = 'john', email = 'john1@example.com',role = ROLE_RESEARCHER)
        u2 = User(nickname = 'john', email = 'john2@example.com',role = ROLE_RESEARCHER)

        survey = Survey(title = "test",researcher = u1)
        s1 = Section (title = "1",description = "a",survey = survey)
        # l=["1","2","3","4","5"]
        # q1 = QuestionChoice(text="q1",section=s1,choices=l)
        q1 = QuestionText(text="q1",section=s1,expectedAnswer="1",maxNumberAttempt=3)

        db.session.add(u1)
        db.session.add(u2)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(q1)
        db.session.commit()

        g.user = u1
        f = generate_form(s1.questions)
        f["c"+str(q1.id)].data="1.5"
        u = CheckAnswerExpected()
        # u.__call__(f,f["c"+str(q1.id)])
        self.assertRaises(ValidationError,u.__call__,f,f["c"+str(q1.id)])
        
        f["c"+str(q1.id)].data="1"
        self.assertIsNone(u.__call__(f,f["c"+str(q1.id)]))

        g.user= u2
        f["c"+str(q1.id)].data="1.5"
        u = CheckAnswerExpected()
        self.assertRaises(ValidationError,u.__call__,f,f["c"+str(q1.id)])
        self.assertRaises(ValidationError,u.__call__,f,f["c"+str(q1.id)])
        self.assertEqual(u.__call__(f,f["c"+str(q1.id)]),flash(u.message_continue))

    def test_check_subquestion(self):
        u1 = User(nickname = 'john', email = 'john1@example.com',role = ROLE_RESEARCHER)
        u2 = User(nickname = 'john', email = 'john2@example.com',role = ROLE_RESEARCHER)

        survey = Survey(title = "test",researcher = u1)
        s1 = Section (title = "1",description = "a",survey = survey)
        # l=["1","2","3","4","5"]
        # q1 = QuestionChoice(text="q1",section=s1,choices=l)
        q1 = QuestionText(text="q1",section=s1)
        condition1=Condition(operation="==",value="0")
        q2 = QuestionYN(text="q2", section=s1, condition=condition1,
            parent = q1)

        l=["1","2","3"]
        q3 = QuestionChoice(text="q1",section=s1,choices=l)
        condition2=Condition(operation="==",value="0")
        q4 = QuestionYN(text="q4", section=s1, condition=condition2,
            parent = q3)
        
        condition3=Condition(operation=">",value="1")
        q5 = QuestionYN(text="q5", section=s1, condition=condition3,
            parent = q3)

        condition4=Condition(operation="<",value="1")
        q6 = QuestionYN(text="q6", section=s1, condition=condition4,
            parent = q3)

        q7 = QuestionYN(text="q7",section=s1)
        condition5=Condition(operation="==",value="yes")
        q8 = QuestionYN(text="q8", section=s1, condition=condition5,
            parent = q7)


        db.session.add(u1)
        db.session.add(u2)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(q1)
        db.session.add(q2)
        db.session.add(q3)
        db.session.add(q4)
        db.session.add(q5)
        db.session.add(q6)
        db.session.add(q7)
        db.session.add(q8)
        db.session.add(condition1)
        db.session.add(condition2)
        db.session.add(condition3)
        db.session.add(condition4)
        db.session.add(condition5)
        db.session.commit()

        g.user = u1
        f = generate_form(s1.questions)
        u = CheckSubquestion()
        # if data == !0 no validate anything(stop validation)
        f["c"+str(q1.id)].data="1"
        f["c"+str(q2.id)].errors=[]        
        self.assertRaises(StopValidation,u.__call__,f,f["c"+str(q2.id)])
        f["c"+str(q1.id)].data="0"
        self.assertIsNone(u.__call__(f,f["c"+str(q2.id)]))

        # if data == !0 no validate anything(stop validation)
        f["c"+str(q3.id)].data="1"
        f["c"+str(q4.id)].errors=[]   #error is a tuple, but expected list     
        self.assertRaises(StopValidation,u.__call__,f,f["c"+str(q4.id)])
        f["c"+str(q3.id)].data="0"
        self.assertIsNone(u.__call__(f,f["c"+str(q4.id)]))


        # if (data < =1), not (data>1)  no validate anything(stop validation)
        f["c"+str(q3.id)].data="1"
        f["c"+str(q5.id)].errors=[]   #error is a tuple, but expected list     
        self.assertRaises(StopValidation,u.__call__,f,f["c"+str(q5.id)])
        f["c"+str(q3.id)].data="2"
        self.assertIsNone(u.__call__(f,f["c"+str(q5.id)]))

        # if data >=1 , not(data<1) no validate anything(stop validation)
        f["c"+str(q3.id)].data="1"
        f["c"+str(q6.id)].errors=[]   #error is a tuple, but expected list     
        self.assertRaises(StopValidation,u.__call__,f,f["c"+str(q6.id)])
        f["c"+str(q3.id)].data="0"
        self.assertIsNone(u.__call__(f,f["c"+str(q6.id)]))


        # if data ==no, not(data==yes) no validate anything(stop validation)
        f["c"+str(q7.id)].data="no"
        f["c"+str(q8.id)].errors=[]   #error is a tuple, but expected list     
        self.assertRaises(StopValidation,u.__call__,f,f["c"+str(q8.id)])
        f["c"+str(q7.id)].data="yes"
        self.assertIsNone(u.__call__(f,f["c"+str(q8.id)]))

    def test_requerid_selectField(self):
        u1 = User(nickname = 'john', email = 'john1@example.com',role = ROLE_RESEARCHER)
        survey = Survey(title = "test",researcher = u1)
        s1 = Section (title = "1",description = "a",survey = survey)
        l=["1","2","3","4","5"]
        q1 = QuestionChoice(text="q1",section=s1,choices=l,render="select")
        db.session.add(u1)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(q1)
        db.session.commit()
      
        f = generate_form(s1.questions)
        u = RequiredSelectField()
        # if data == !0 no validate anything(stop validation)
        f["c"+str(q1.id)].data=""
        self.assertRaises(ValidationError,u.__call__,f,f["c"+str(q1.id)])
        f["c"+str(q1.id)].data="0"
        self.assertIsNone(u.__call__(f,f["c"+str(q1.id)]))

if __name__ == '__main__':
    unittest.main()