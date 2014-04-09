from app.models import StateSurvey, Answer, Section, Question, User, Survey
from app.models import GameImpatience, GameLottery1, GameLottery2
from app.models import GameRent1, GameRent2, GameUltimatum, GameDictador
from sqlalchemy import or_
import random
from app import db, models


class Games:
    '''find all game in a survey
        Automatice matching between games
    '''
    MIN_USER_MATCH = 10 #8 is sufficient
    def __init__(self, survey_id):
        self.survey=Survey.query.get(survey_id)
        self.part2_money=self._find_part2(True)
        self.part2_no_money=self._find_part2(False)
        self.decision1_v1_money=self._find_decision("decision_one_v1",True)
        self.decision1_v1_no_money=self._find_decision("decision_one_v1",False)
        self.decision1_v2_money=self._find_decision("decision_one_v2",True)
        self.decision1_v2_no_money=self._find_decision("decision_one_v2",False)

        self.decision2_money=self._find_decision("decision_two",True)
        self.decision2_no_money=self._find_decision("decision_two",False)
        self.decision3_money=self._find_decision("decision_three",True)
        self.decision3_no_money=self._find_decision("decision_three",False)
        self.decision4_money=self._find_decision("decision_four",True)
        self.decision4_no_money=self._find_decision("decision_four",False)
        self.decision5_money=self._find_section_decision5(True)
        self.decision5_no_money=self._find_section_decision5(False)
        self.decision6_money=self._find_decision("decision_six",True)
        self.decision6_no_money=self._find_decision("decision_six",False)

    def __repr__(self):
        return "<Games(part_two_money='%s', part_two_without_money='%s'\n\
            decision_one_money='%s',decision_one_without_money='%s' \n\
            decision_two_money='%s',decision_two_without_money='%s' \n\
            decision_three_money='%s',decision_three_without_money='%s' \n\
            decision_four_money='%s',decision_four_without_money='%s' \n\
            decision_five_money='%s',decision_five_without_money='%s' \n\
            decision_six_money='%s',decision_six_without_money='%s')>" % (
            self.part2_money, self.part2_without_money,\
            self.decision1_v1_money, self.decision1_v1_no_money,\
            self.decision1_v2_money, self.decision1_v2_no_money,\
            self.decision2_money, self.decision2_no_money,\
            self.decision3_money, self.decision3_no_money,\
            self.decision4_money, self.decision4_no_money,\
            self.decision5_money, self.decision5_no_money,\
            self.decision6_money, self.decision6_no_money)

    def _find_decision(self,decision,with_money):
        return Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision==decision,\
            Question.is_real_money==with_money).first()

    def _find_section_decision_5(self,with_money):
        q = Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision=="decision_five",\
            Question.is_real_money==with_money).first()
        return q.section
    
    def _find_part2(self,with_money):
        return [q.id for q in Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision=="part_two",\
            Question.is_real_money==with_money)]
    
    def _match_decision1_v1_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question = self.decision1_v1_money
        else:
            question = self.decision1_v1_no_money
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()        
        game = GameLottery1(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    def _match_decision1_v2_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question = self.decision1_v2_money
        else:
            question = self.decision1_v2_no_money
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()        
        game = GameLottery2(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)


    def _match_decision2_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question = self.decision2_money
        else:
            question = self.decision2_no_money

        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
        game = GameRent1(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)
   
    def _match_decision3_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question = self.decision3_money
        else:
            question = self.decision3_no_money

        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
        game = GameRent2(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    def _match_decision4_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question4 = self.decision4_money
            section5 = self.decision5_money
        else:
            question4 = self.decision4_no_money
            section5 = self.decision5_no_money

        answerA = Answer.query.filter_by(user_id=userA,question_id=question4.id).first()
        game = GameUltimatum(userA=userA, userB=userB,\
            answerA = answerA.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id, section = section5)
        db.session.add(game)

    def _match_decision6_users(self,userA,userB,money,repeatA=False,repeatB=False):
        if money:
            question = self.decision6_money
        else:
            question = self.decision6_no_money

        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        game = GameDictador(userA=userA, userB=userB,\
            answerA = answerA.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    






















    def part2(self,user):
        '''select random answer to game of part2 (GameImpatience)
            store in db
        '''
        ans = Answer.query.filter(\
            Answer.user_id==user.id,\
            Answer.question_id==self.part_two_money[0]).first()
        if ans is not None:
            #game with real money
            question = random.choice(self.part_two_money)
            status = StateSurvey.PART_TWO_MONEY
            is_real_money=True
        else:
            question = random.choice(self.part_two_without_money)
            status = StateSurvey.PART_TWO_WITHOUT_MONEY
            is_real_money=False

        answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
        game = GameImpatience(user=user.id, answer = answer.id,\
            survey=self.survey.id, is_real_money=is_real_money)
        state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
            StateSurvey.user_id==user.id).first()
        state_survey.status=state_survey.status | status

        db.session.add(game)
        db.session.add(state_survey)
        db.session.commit()