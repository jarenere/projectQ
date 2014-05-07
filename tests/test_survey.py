from __future__ import division

import unittest
from sqlalchemy.exc import IntegrityError
from flask import current_app
from app import app,db
from app.models import User,ROLE_RESEARCHER
from app.models import Survey, Section, Consent,Question
from app.models import QuestionChoice,QuestionText
from app.models import QuestionLikertScale, QuestionYN
from app.models import Condition
from app.models import Answer
from app.models import GameImpatience
from app.models import GameLottery1, GameLottery2
import tempfile
import os
from config import basedir

def check_sequence(dic):
    '''return true if all values>0'''
    for i in dic.values():
        if i==0:
            return False
    return True

class ModelsTestCase(unittest.TestCase):
    '''test models'''



    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()



    # def test_sequence_sections_exclusive(self):
    #     '''test function  sequenceSections(sections)'''

    #     # create a user
    #     u = User(nickname = 'john', email = 'john@example.com', 
    #         role = ROLE_RESEARCHER)
    #     db.session.add(u)    
    #     survey = Survey(title = "test",researcher = u)
    #     s1 = Section (title = "1",description = "a",
    #         sequence = 1, percent = 1, survey = survey)
    #     s11 = Section (title = "1.1", description = "a",
    #         sequence = 1, percent = 0.5, parent = s1)
    #     s12 = Section (title = "1.1", description = "a",
    #         sequence = 1, percent = 0.5, parent = s1)
    #     s111 = Section (title = "1.1", description = "a",
    #         sequence = 1, percent = 0.5, parent = s11)
    #     s112 = Section (title = "1.1", description = "a",
    #         sequence = 1, percent = 0.5, parent = s11)
    #     db.session.add(survey)
    #     db.session.add(s1)
    #     db.session.add(s11)
    #     db.session.add(s12)
    #     db.session.add(s111)
    #     db.session.add(s112)
    #     db.session.commit()
    #     # key1 0.25 %
    #     key1 = (s1.id,s11.id,s111.id)
    #     # key2 0.25 %
    #     key2 =  (s1.id,s11.id,s112.id)
    #     # key3 0.50 %
    #     key3 = (s1.id,s12.id)
    #     dic ={key1:0,key2:0,key3:0}
    #     n = 100
    #     error = 0.1
    #     for i in range(n):
    #         l = tuple(Section.sequenceSections(survey.sections))
    #         if dic.has_key(l):
    #             dic[l] = dic[l]+1
    #         else:
    #             self.assertTrue(False,"unexpected value")
    #     self.assertTrue(check_sequence(dic))
    #     range1 = range(int(round(n*.25 - error*n)),int(round(n*.25 + error*n)))
    #     range2 = range(int(round(n*.5 - error*n)),int(round(n*.5 + error*n)))
    #     self.assertTrue(dic[key1] in range1)
    #     self.assertTrue(dic[key2] in range1)
    #     self.assertTrue(dic[key3] in range2)

    # def test_sequence_sections_order(self):
    #     '''test function  sequenceSections(sections)'''
    #     u = User(nickname = 'john', email = 'john1@example.com', 
    #         role = ROLE_RESEARCHER)
    #     db.session.add(u)
    #     survey = Survey(title = "test",researcher = u)
    #     s1 = Section (title = "1",description = "a",
    #         sequence = 1, percent = 1, survey = survey)
    #     s2 = Section (title = "1",description = "a",
    #         sequence = 2, percent = 1, survey = survey)
    #     s3 = Section (title = "1",description = "a",
    #         sequence = 2, percent = 1, survey = survey)
    #     s4 = Section (title = "1",description = "a",
    #         sequence = 2, percent = 1, survey = survey)
    #     s5 = Section (title = "1",description = "a",
    #         sequence = 3, percent = 1, survey = survey)
    #     s6 = Section (title = "1",description = "a",
    #         sequence = 3, percent = 1, survey = survey)
    #     db.session.add(survey)
    #     db.session.add(s1)
    #     db.session.add(s2)
    #     db.session.add(s3)
    #     db.session.add(s4)
    #     db.session.add(s5)
    #     db.session.add(s6)
    #     db.session.commit()
    #     s1 = s1.id
    #     s2 = s2.id
    #     s3 = s3.id
    #     s4 = s4.id
    #     s5 = s5.id
    #     s6 = s6.id
    #     key1 = (s1,s2,s3,s4,s5,s6)
    #     key2 = (s1,s2,s3,s4,s6,s5)
    #     key3 = (s1,s2,s4,s3,s5,s6)
    #     key4 = (s1,s2,s4,s3,s6,s5)
    #     key5 = (s1,s3,s2,s4,s5,s6)
    #     key6 = (s1,s3,s2,s4,s6,s5)
    #     key7 = (s1,s3,s4,s2,s5,s6)
    #     key8 = (s1,s3,s4,s2,s6,s5)
    #     key9 = (s1,s4,s2,s3,s5,s6)
    #     key10 = (s1,s4,s2,s3,s6,s5)
    #     key11 = (s1,s4,s3,s2,s5,s6)
    #     key12 = (s1,s4,s3,s2,s6,s5)
    #     dic = {key1:0,key2:0,key3:0,key4:0,key5:0,key6:0,key7:0,
    #         key8:0,key9:0,key10:0,key11:0,key12:0}
    #     n = 100
    #     i=0
    #     while not check_sequence(dic) and i<n:
    #         l = tuple(Section.sequenceSections(survey.sections))
    #         if dic.has_key(l):
    #             dic[l] = dic[l]+1
    #         else:
    #             self.assertTrue(False,"unexpected value")
    #     i=i+1
    #     self.assertTrue(check_sequence(dic))

    # def test_import_export(self):
    #     u = User(nickname = 'john', email = 'john1@example.com', 
    #         role = ROLE_RESEARCHER)
    #     db.session.add(u)
    #     survey = Survey(title = "test",researcher = u)
    #     db.session.add(survey)
    #     consent = Consent(text="a", survey=survey)
    #     db.session.add(consent)
    #     s1 = Section (title = "1",description = "a",
    #         sequence = 1, percent = 1, survey = survey)
    #     db.session.add(s1)
    #     s11 = Section (title = "11", description = "a",
    #         sequence = 1, percent = 0.5, parent = s1)
    #     db.session.add(s11)
    #     s12 = Section (title = "12", description = "a",
    #         sequence = 1, percent = 0.5, parent = s1)
    #     db.session.add(s12)
    #     s111 = Section (title = "111", description = "a",
    #         sequence = 1, parent = s11)
    #     db.session.add(s111)
    #     s112 = Section (title = "112", description = "a",
    #         sequence = 2, parent = s11)
    #     db.session.add(s112)
    #     q1 = QuestionText(text="q1",section=s1)
    #     db.session.add(q1)

    #     q2 = QuestionChoice(text="q2",section=s11,range_min=1,range_max=10)
    #     db.session.add(q2)
    #     l=["thing1","thing2","thing3"]  
    #     q3 = QuestionChoice(text="q3",section=s11,choices =l)
    #     db.session.add(q3)
    #     condition=Condition(operation="==",value=0)
    #     q4 = QuestionYN(text="q4", section=s11, condition=condition,
    #         parent = q3)
    #     db.session.add(q4)
    #     q5 = QuestionLikertScale(text="q5",minLikert =1,maxLikert=7,
    #         labelMin="min",labelMax="max", section=s112)
    #     db.session.add(q5)
    #     db.session.commit()
    #     xml = survey.to_xml()
    #     tf = tempfile.NamedTemporaryFile()
    #     xml.write(tf.name,encoding="ISO-8859-1", method="xml")

    #     msg,s = Survey.from_xml(tf.name,u)

    #     self.assertTrue(s.title == survey.title)
    #     self.assertTrue(s.consents.first().text == survey.consents.first().text)
    #     j = Section.query.filter(Section.title=="1",Section.root==s).first()
    #     self.assertTrue(j.percent==s1.percent)
    #     j = Section.query.filter(Section.title=="112",Section.root==s).first()
    #     self.assertTrue(j.sequence==s112.sequence)
    #     q = Question.query.filter(Question.text=="q3",
    #         Question.section_id==Section.id,Section.root==s).first()
    #     self.assertTrue(len(q.choices)==3)
    #     q = Question.query.filter(Question.text=="q4",
    #         Question.section_id==Section.id,Section.root==s).first()
    #     self.assertTrue(q.isSubquestion)
    #     self.assertFalse(q.isExpectedAnswer())
    #     self.assertTrue(q.section.title==q4.section.title)

    # def test_question_expected(self):
    #     u = User(nickname = 'john', email = 'john1@example.com', 
    #         role = ROLE_RESEARCHER)
    #     db.session.add(u)
    #     survey = Survey(title = "test",researcher = u)
    #     db.session.add(survey)
    #     s1 = Section (title = "1",description = "a",
    #         sequence = 1, percent = 1, survey = survey)
    #     db.session.add(s1)
    #     q1 = QuestionText(text="q1",section=s1,expectedAnswer="1",maxNumberAttempt=3)
    #     db.session.add(q1)
    #     db.session.commit()
    #     ans = Answer(user=u,question=q1,answerText="2")
    #     db.session.add(ans)
    #     db.session.commit()
    #     self.assertFalse(ans.answerAttempt())
    #     self.assertTrue(ans.isMoreAttempt())
    #     ans.answerText="1"
    #     self.assertTrue(ans.answerAttempt())
    #     ans.numberAttempt=4
    #     self.assertFalse(ans.isMoreAttempt())
    #     q2 = QuestionYN(text="q1",section=s1,expectedAnswer="yes",maxNumberAttempt=0)
    #     db.session.add(q2)
    #     ans = Answer(user=u,question=q2,answerYN=False)
    #     db.session.add(ans)
    #     db.session.commit()
    #     self.assertTrue(ans.isMoreAttempt())
    #     self.assertFalse(ans.answerAttemptYN())
    #     ans.answerYN=True
    #     self.assertTrue(ans.answerAttemptYN())


    def test_game_impatience(self):
        u = User(nickname = 'john', email = 'john1@example.com', 
            role = ROLE_RESEARCHER)
        db.session.add(u)
        survey = Survey(title = "test",researcher = u)
        db.session.add(survey)
        s1 = Section (title = "1",description = "a", survey = survey)
        db.session.add(s1)
        q1 = QuestionText(text="q1",section=s1)
        db.session.add(q1)
        ans = Answer(user=u,question=q1,answerText="2")
        db.session.add(ans)
        db.session.commit()

        n=100
        i=0
        first_value = False
        second_value = True 
        first_value_received = False
        second_value_received = False
        while i<n and (not first_value_received or not second_value_received):
            game = GameImpatience(survey = survey,
                user= u,
                answer = ans,
                is_real_money=True)
            db.session.add(game)
            db.session.commit()
            if not first_value_received:
                first_value_received = first_value== game.prize
            if not second_value_received:
                second_value_received = second_value == game.prize
            db.session.delete(game)
            db.session.commit()
            i=i+1
        self.assertTrue(first_value_received and second_value_received)

        game = GameImpatience(survey = survey,
            user= u,
            answer = ans,
            is_real_money=True)
        db.session.add(game)
        db.session.commit()
        game = GameImpatience(survey = survey,
            user= u,
            answer = ans,
            is_real_money=True)
        db.session.add(game)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        game = GameImpatience(survey = survey,
            user= u,
            answer = ans,
            is_real_money=True)
        
        # Game.user should not be nullable
        game.user=None
        db.session.add(game)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        # Game.survey should not be nullable
        game.survey=None
        db.session.add(game)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        # Game.answer should not be nullable
        game.answer=None
        db.session.add(game)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()


    def test_game_lottery1(self):
        u1 = User(nickname = 'john', email = 'john1@example.com',role = ROLE_RESEARCHER)
        u2 = User(nickname = 'john', email = 'john2@example.com')
        survey = Survey(title = "test",researcher = u)
        s1 = Section (title = "1",description = "a",survey = survey)
        q1 = QuestionText(text="q1",section=s1)
        ans1 = Answer(user=u1,question=q1,answerText="1.5")
        ans2 = Answer(user=u2,question=q1,answerText="2.5")
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(q1)
        db.session.add(ans1)


        db.session.add(ans2)
        GameLottery2







if __name__ == '__main__':
    unittest.main()