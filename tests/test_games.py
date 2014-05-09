from __future__ import division

import unittest
from app import app,db
from app.models import User,ROLE_RESEARCHER
from app.models import Survey, Question, GameImpatience, StateSurvey
import os
from config import basedir
from app.game.game import Games
import datetime


class GamesTestCase(unittest.TestCase):
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

    def test_find_questions(self):
        u = User(nickname = 'john', email = 'john1@example.com', 
            role = ROLE_RESEARCHER)
        db.session.add(u)
        db.session.commit()
        base=os.path.abspath(os.path.dirname(__file__))
        name = "como_son_nuestros_voluntarios_only_games.xml"
        msg,s = Survey.from_xml(os.path.join(base,name),u)
        game = Games(s.id)

        self.assertIsNotNone(game.select_game["part2",True])
        self.assertIsNotNone(game.select_game["part2",False])
        self.assertIsNotNone(game.select_game["decision1_v1",True])
        self.assertIsNotNone(game.select_game["decision1_v1",False])
        self.assertIsNotNone(game.select_game["decision2",True])
        self.assertIsNotNone(game.select_game["decision2",False])
        self.assertIsNotNone(game.select_game["decision3",True])
        self.assertIsNotNone(game.select_game["decision3",False])
        self.assertIsNotNone(game.select_game["decision4",True])
        self.assertIsNotNone(game.select_game["decision4",False])
        self.assertIsNotNone(game.select_game["decision5",True])
        self.assertIsNotNone(game.select_game["decision5",False])
        self.assertIsNotNone(game.select_game["decision6",True])
        self.assertIsNotNone(game.select_game["decision6",False])

        qs = Question.query.filter(Question.decision=="decision_two")
        for q in qs:
            db.session.delete(q)
        db.session.commit()
        game = Games(s.id)
        self.assertIsNone(game.select_game["decision2",True])
        self.assertIsNone(game.select_game["decision2",False])

    def test_matching(self):
        import utiles
        u = User(nickname = 'john', email = 'john1@example.com', 
            role = ROLE_RESEARCHER)
        db.session.add(u)
        db.session.commit()
        base=os.path.abspath(os.path.dirname(__file__))
        name = "como_son_nuestros_voluntarios_only_games.xml"
        msg,s = Survey.from_xml(os.path.join(base,name),u)
        game = Games(s.id)
        s.endDate = s.endDate + datetime.timedelta(1,0)
        db.session.add(s)
        db.session.commit()
        n1=40
        utiles.generate_answers_fake(s.id, n1)
        game.match()
        users = StateSurvey.query.filter(StateSurvey.survey_id==s.id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.PART2_MONEY)==0,\
            StateSurvey.status.op('&')(StateSurvey.PART2_NO_MONEY)==0)
        for u in users:
            game.part2(u.user)
            game.raffle(u.user)
        self.assertEqual(n1,len(GameImpatience.query.all()))
        
        n2 = 1
        utiles.generate_answers_fake(s.id, n2)
        game.match()
        users = StateSurvey.query.filter(StateSurvey.survey_id==s.id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.PART2_MONEY)==0,\
            StateSurvey.status.op('&')(StateSurvey.PART2_NO_MONEY)==0)
        for u in users:
            game.part2(u.user)
            game.raffle(u.user)
        self.assertEqual(n1+n2,len(GameImpatience.query.all()))


if __name__ == '__main__':
    unittest.main()