from app.models import StateSurvey, Answer, Section, Question, User, Survey
from app.models import GameImpatience, GameLottery1, GameLottery2
from app.models import GameRent1, GameRent2, GameUltimatum, GameDictador
from app.models import Game
from sqlalchemy import or_
import random
from app import db, models


class Games:
    '''find all game in a survey
        Automatice matching between games
    '''
    MIN_USERS_PART3 = 10 #8 is sufficient
    MIN_USERS_DECISION1_V1 = 4
    MIN_USERS_DECISION1_V2 = 4
    def __init__(self, survey_id):
        self.survey = Survey.query.get(survey_id)
        self.select_game = {}
        self.select_game["part2",True] = self._find_part2(True)
        self.select_game["part2",False] = self._find_part2(False)
        self.select_game["decision1_v1",True] = self._find_decision("decision_one_v1",True)
        self.select_game["decision1_v1",False] = self._find_decision("decision_one_v1",False)
        self.select_game["decision1_v2",True] = self._find_decision("decision_one_v2",True)
        self.select_game["decision1_v2",False] = self._find_decision("decision_one_v2",False)
        self.select_game["decision2",True] = self._find_decision("decision_two",True)
        self.select_game["decision2",False] = self._find_decision("decision_two",False)
        self.select_game["decision3",True] = self._find_decision("decision_three",True)
        self.select_game["decision3",False] = self._find_decision("decision_three",False)
        self.select_game["decision4",True] = self._find_decision("decision_four",True)
        self.select_game["decision4",False] = self._find_decision("decision_four",False)
        self.select_game["decision5",True] = self._find_section_decision5(True)
        self.select_game["decision5",False] = self._find_section_decision5(False)
        self.select_game["decision6",True] = self._find_decision("decision_six",True)
        self.select_game["decision6",False] = self._find_decision("decision_six",False)
        self.status ={}
        self.status["part2",True] = StateSurvey.PART2_MONEY
        self.status["part2",False] = StateSurvey.PART2_NO_MONEY       
        self.status["part3",True] = StateSurvey.PART3_MONEY
        self.status["part3",False] = StateSurvey.PART3_NO_MONEY
        self.status["part2"] = StateSurvey.GAME_IMPATIENCE
        self.status["decision1_v1"] = StateSurvey.GAME_LOTTERY_V1
        self.status["decision1_v2"] = StateSurvey.GAME_LOTTERY_V2
        self.status["decision2"] = StateSurvey.GAME_RENT1
        self.status["decision3"] = StateSurvey.GAME_RENT2
        self.status["decision4"] = StateSurvey.GAME_ULTIMATUM
        self.status["decision6"] = StateSurvey.GAME_DICTADOR
        self.status["match"] = StateSurvey.MATCHING

    def __repr__(self):
        return "<Games(part_two_money='%s', part_two_without_money='%s'\n\
            decision_one_v1_money='%s',decision_one_v1_without_money='%s' \n\
            decision_one_v2_money='%s',decision_one_v2_without_money='%s' \n\
            decision_two_money='%s',decision_two_without_money='%s' \n\
            decision_three_money='%s',decision_three_without_money='%s' \n\
            decision_four_money='%s',decision_four_without_money='%s' \n\
            decision_five_money='%s',decision_five_without_money='%s' \n\
            decision_six_money='%s',decision_six_without_money='%s')>" % (
            self.select_game["part2",True], self.select_game["part2",False],\
            self.select_game["decision1_v1",True],self.select_game["decision1_v1",False],\
            self.select_game["decision1_v2",True], self.select_game["decision1_v2",False],\
            self.select_game["decision2",True],self.select_game["decision2",False],\
            self.select_game["decision3",True], self.select_game["decision3",False],\
            self.select_game["decision4",True], self.select_game["decision4",False],\
            self.select_game["decision5",True], self.select_game["decision5",False],\
            self.select_game["decision6",True], self.select_game["decision6",False])

    def _find_decision(self,decision,with_money):
        return Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision==decision,\
            Question.is_real_money==with_money).first()

    def _find_section_decision5(self,with_money):
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
        question = self.select_game["decision1_v1",money]
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()        
        game = GameLottery1(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    def _match_decision1_v2_users(self,userA,userB,money,repeatA=False,repeatB=False):
        question = self.select_game["decision1_v2",money]
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()        
        game = GameLottery2(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)


    def _match_decision2_users(self,userA,userB,money,repeatA=False,repeatB=False):
        question = self.select_game["decision2",money]
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
        game = GameRent1(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)
   
    def _match_decision3_users(self,userA,userB,money,repeatA=False,repeatB=False):
        question = self.select_game["decision3",money]
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
        game = GameRent2(userA=userA, userB=userB,\
            answerA = answerA.id, answerB = answerB.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    def _match_decision4_users(self,userA,userB,money,repeatA=False,repeatB=False):
        question4 = self.select_game["decision4",money]
        section5 = self.select_game["decision5",money].id
        answerA = Answer.query.filter_by(user_id=userA,question_id=question4.id).first()
        game = GameUltimatum(userA=userA, userB=userB,\
            answerA = answerA.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id, section = section5)
        db.session.add(game)

    def _match_decision6_users(self,userA,userB,money,repeatA=False,repeatB=False):
        question = self.select_game["decision6",money]
        answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
        game = GameDictador(userA=userA, userB=userB,\
            answerA = answerA.id,\
            repeatA = repeatA, repeatB = repeatB,\
            survey=self.survey.id)
        db.session.add(game)

    def _users_part3_no_match(self, money):
        question_id = self.select_game["decision2",money].id
        return [ss.user_id for ss in StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.MATCHING)==0,\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==question_id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)]
    
    def _users_part3_match(self, money):
        question_id = self.select_game["decision2",money].id
        return [ss.user_id for ss in StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.MATCHING),\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==question_id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)]
    
    def _users_decision_no_match(self,decision, money):
        question_id = self.select_game[decision,money].id
        return [ss.user_id for ss in StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(self.status[decision])==0,\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==question_id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)]

    def _users_decision_match(self,decision, money):
        question_id = self.select_game[decision,money].id
        return [ss.user_id for ss in StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(self.status[decision]),\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==question_id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)]

    def _flag_status(self,user,status):
        ss = StateSurvey.query.filter(\
            StateSurvey.user_id==user,\
            StateSurvey.survey_id==self.survey.id).first()
        ss.status=ss.status | self.status[status]
        db.session.add(ss)

    def _prize_decision1(self,user):
        game = Game.query.filter(\
            Game.survey==self.survey.id,\
            or_(Game.type=="gameLottery1",Game.type=="gameLottery2"),\
            or_(Game.userA==user, Game.userB==user)).first()
        if game.userA==user:
            game.prizeA=True
        elif game.userB==user:
            game.prizeB=True
        else:
            raise "error, user in decision one not found"
        db.session.add(game)

    def _prize_decision2_3(self,user,decision):
        game = Game.query.filter(\
            Game.survey==self.survey.id,\
            Game.type==decision,\
            or_(Game.userA==user, Game.userB==user)).first()
        if game.userA==user:
            game.prizeA=True
        elif game.userB==user:
            game.prizeB=True
        else:
            raise "error, user in decision one not found"
        db.session.add(game)

    def _prize_decision4_6_playerA(self,user,decision):
        game = Game.query.filter(\
            Game.survey==self.survey.id,\
            Game.type==decision,\
            Game.userA==user).first()
        game.prizeA=True
        db.session.add(game)

    def _prize_decision4_6_playerB(self,user,decision):
        game = Game.query.filter(\
            Game.survey==self.survey.id,\
            Game.type==decision,\
            Game.userB==user).first()
        game.prizeB=True
        db.session.add(game)

    def _prize(self,user):
        # can be implementated with dictionary, but lamba functions haven input parameters
        if random.randint(1,10)==1:
            #user prize
            n=random.randint(1,7)
            if n==1:
                self._prize_decision1(user)
            elif n==2:
                self._prize_decision2_3(user,"gameRent1")
            elif n==3:
                self._prize_decision2_3(user,"gameRent2")
            elif n==4:
                self._prize_decision4_6_playerA(user,"gameUltimatum")
            elif n==5:
                self._prize_decision4_6_playerA(user,"gameUltimatum")
            elif n==6:
                self._prize_decision4_6_playerA(user,"gameDictador")
            elif n==7:
                self._prize_decision4_6_playerA(user,"gameDictador")

    def _match_alone_user(self,decision,user, money):
        if decision == "decision1_v1":
            self._match_decision1_v1_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
        elif decision == "decision1_v2":
            self._match_decision1_v2_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
        elif decision == "decision2":
            self._match_decision2_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
        elif decision == "decision3":
            self._match_decision3_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
        elif decision == "decision4":
            self._match_decision4_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
            self._match_decision4_users(
                random.choice(self._users_decision_match(decision, money)),user,
                money,repeatA=True, repeatB=False)
        elif decision == "decision6":
            self._match_decision6_users(user,
                random.choice(self._users_decision_match(decision, money)),
                money,repeatA=False, repeatB=True)
            self._match_decision6_users(
                random.choice(self._users_decision_match(decision, money)),user,
                money,repeatA=True, repeatB=False)
        else:
            raise "error, bad decision"
        self._flag_status(user,decision)




    def _match(self,decision,users, money):
        def generate_tuple(users):
            '''can succes-> l[i][0]==l[i][1]
            '''
            l_aux1=users[:]
            l_aux2=users[:]
            l=[]
            for i in range(len(users)):
                userA = random.choice(l_aux1)
                userB = random.choice(l_aux2)
                l_aux1.remove(userA)
                l_aux2.remove(userB)
                l.append((userA,userB))
            return l

        if decision=="decision1_v1" or decision=="decision1_v2" or\
                decision=="decision2" or decision=="decision3":
            if len(users)%2==0:
                alone_user=None
            else:
                alone_user = users[-1]
                users = users[:-1]
            for i in range(len(users)/2):
                print i, "of", len(users)/2, decision
                userA = random.choice(users)
                users.remove(userA)
                userB = random.choice(users)
                users.remove(userB)
                if decision == "decision1_v1":
                    self._match_decision1_v1_users(userA,userB,money)
                elif decision == "decision1_v2":
                    self._match_decision1_v2_users(userA,userB,money)
                elif decision == "decision2":
                    self._match_decision2_users(userA,userB,money)
                elif decision == "decision3":
                    self._match_decision3_users(userA,userB,money)
                self._flag_status(userA, decision)
                self._flag_status(userB, decision)
            db.session.commit()
            if alone_user is not None:
                self._match_alone_user(decision, alone_user, money)
                db.session.commit()
        
        elif decision=="decision4" or decision=="decision6":
            tuple_users = generate_tuple(users)
            for i in tuple_users:
                print i, "of", decision

                if decision=="decision4":
                    self._match_decision4_users(i[0], i[1], money)
                elif decision=="decision6":
                    self._match_decision6_users(i[0], i[1], money)
            for user in users : self._flag_status(user, decision)
            db.session.commit()
        else:
            raise "error, decision invalid", decision

    def filter_decision1(self,users,money):
        users_decision1_v1=[]
        users_decision1_v2=[]
        question_id = self.select_game["decision1_v1",money].id
        for user in users:
            if User.query.filter(\
                    Answer.question_id==question_id,\
                    Answer.user_id==user).first() is not None:
                users_decision1_v1.append(user)
            else:
                users_decision1_v2.append(user)
        return users_decision1_v1,users_decision1_v2

    def matching(self, money):
        users_part3_no_match = self._users_part3_no_match(money=money)
        users_decision1_v1,users_decision1_v2 = self.filter_decision1(users_part3_no_match,money)

        do = False
        if len(users_part3_no_match) >self.MIN_USERS_PART3 and \
                len(users_decision1_v1)>self.MIN_USERS_DECISION1_V1 and\
                len(users_decision1_v2)>self.MIN_USERS_DECISION1_V2:
            print users_part3_no_match, users_decision1_v1 ,users_decision1_v2
            self._match("decision1_v1",users_decision1_v1[:],money)
            self._match("decision1_v2",users_decision1_v2[:],money)
            self._match("decision2",users_part3_no_match[:],money)
            self._match("decision3",users_part3_no_match[:],money)
            self._match("decision4",users_part3_no_match[:],money)
            self._match("decision6",users_part3_no_match[:],money)
            do = True
        else:
            users_part3_match=self._users_part3_match(money)
            if len(users_part3_match)>=self.MIN_USERS_PART3:
                for user in users_part3_no_match:
                    question = self.select_game["decision1_v1",money]
                    if Answer.query.filter_by(user_id =user,\
                            question_id=question.id).first() is not None:
                        self._match_alone_user("decision1_v1",user, money)
                    else:
                        self._match_alone_user("decision1_v2",user, money)
                    self._match_alone_user("decision2",user, money)
                    self._match_alone_user("decision3",user, money)
                    self._match_alone_user("decision4",user, money)
                    self._match_alone_user("decision6",user, money)
                    db.session.commit()
                do =True
        
        if do:
            if money:
                for user in users_part3_no_match: self._prize(user)

            for user in users_part3_no_match: 
                self._flag_status(user, "match")
                self._flag_status(user,("part3",money))


    def match(self):
        self.matching(True)
        self.matching(False)

    def part2(self,user):
        '''select random answer to game of part2 (GameImpatience)
            store in db
        '''
        ans = Answer.query.filter(\
            Answer.user_id==user.id,\
            Answer.question_id==self.select_game["part2",True][0]).first()
        if ans is not None:
            #game with real money
            question = random.choice(self.select_game["part2",True])
            is_real_money=True
        else:
            question = random.choice(self.select_game["part2",False])
            is_real_money=False

        answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
        game = GameImpatience(user=user.id, answer = answer.id,\
            survey=self.survey.id, is_real_money=is_real_money)
        self._flag_status(user.id, ("part2",is_real_money))
        db.session.add(game)
        db.session.commit()