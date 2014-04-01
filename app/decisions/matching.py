from app.models import StateSurvey, Answer, Section, Question, Match, User, Survey
from sqlalchemy import or_
import random
from app import db, models


class Games:
    MIN_USER_MATCH = 6
    def __init__(self, survey_id):
        self.survey=Survey.query.get(survey_id)
        self.part_two_money=self._find_part_two(True)
        self.part_two_without_money=self._find_part_two(False)
        self.decision_one_money=self._find_decision("decision_one",True)
        self.decision_one_without_money=self._find_decision("decision_one",False)
        self.decision_two_money=self._find_decision("decision_two",True)
        self.decision_two_without_money=self._find_decision("decision_two",False)
        self.decision_three_money=self._find_decision("decision_three",True)
        self.decision_three_without_money=self._find_decision("decision_three",False)
        self.decision_four_money=self._find_decision("decision_four",True)
        self.decision_four_without_money=self._find_decision("decision_four",False)
        self.decision_five_money=self._find_section_decision_five(True)
        self.decision_five_without_money=self._find_section_decision_five(False)
        self.decision_six_money=self._find_decision("decision_six",True)
        self.decision_six_without_money=self._find_decision("decision_six",False)

    def __repr__(self):
        return "<Games(part_two_money='%s', part_two_without_money='%s'\n\
            decision_one_money='%s',decision_one_without_money='%s' \n\
            decision_two_money='%s',decision_two_without_money='%s' \n\
            decision_three_money='%s',decision_three_without_money='%s' \n\
            decision_four_money='%s',decision_four_without_money='%s' \n\
            decision_five_money='%s',decision_five_without_money='%s' \n\
            decision_six_money='%s',decision_six_without_money='%s')>" % (
            self.part_two_money, self.part_two_without_money,\
            self.decision_one_money, self.decision_one_without_money,\
            self.decision_two_money, self.decision_two_without_money,\
            self.decision_three_money, self.decision_three_without_money,\
            self.decision_four_money, self.decision_four_without_money,\
            self.decision_five_money, self.decision_five_without_money,\
            self.decision_six_money, self.decision_six_without_money)

    def _find_decision(self,decision,with_money):
        return Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision==decision,\
            Question.is_real_money==with_money).first()
    def _find_section_decision_five(self,with_money):
        q = Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision=="decision_five",\
            Question.is_real_money==with_money).first()
        return q.section
    def _find_part_two(self,with_money):
        l=[q.id for q in Question.query.filter(\
            Question.section_id==Section.id,\
            Section.root_id==self.survey.id,\
            Question.decision=="part_two",\
            Question.is_real_money==with_money)]
        return l
    
    def _users_part_three_money(self):
        state_surveys = StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.MATCHING)==0,\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==self.decision_one_money.id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)
        l=[]
        if state_surveys.count()%2 == 0:
            for ss in state_surveys:
                l.append(ss.user_id)
                ss.status=ss.status | StateSurvey.MATCHING |\
                    StateSurvey.PART_THREE_MONEY
                db.session.add(ss)
        else:
            # impar, last user out!
            for ss in state_surveys[:-1]:
                l.append(ss.user_id)
                ss.status=ss.status | StateSurvey.MATCHING |\
                    StateSurvey.PART_THREE_MONEY
                db.session.add(ss)
        return l

    def _users_part_three_without_money(self):
        state_surveys = StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.status.op('&')(StateSurvey.MATCHING)==0,\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==self.decision_one_without_money.id, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)
        l=[]
        if state_surveys.count()%2 == 0:
            for ss in state_surveys:
                l.append(ss.user_id)
                ss.status=ss.status | StateSurvey.MATCHING |\
                    StateSurvey.PART_THREE_WITHOUT_MONEY
                db.session.add(ss)
        else:
            # impar, last user out!
            for ss in state_surveys[:-1]:
                l.append(ss.user_id)
                ss.status=ss.status | StateSurvey.MATCHING |\
                    StateSurvey.PART_THREE_WITHOUT_MONEY
                db.session.add(ss)
        return l

    def _generate_tupla(self,list_users):
        '''can succes-> l[i][0]==l[i][1]
        '''
        l_aux1=list_users[:]
        l_aux2=list_users[:]
        l=[]
        for i in range(len(list_users)):
            userA = random.choice(l_aux1)
            userB = random.choice(l_aux2)
            l_aux1.remove(userA)
            l_aux2.remove(userB)
            l.append((userA,userB))
        return l
    def _match_decision_one(self,list_users, money):
        # pop two in two
        for i in range(len(list_users)/2):
            print i, "of", len(list_users)/2, "decision one"
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            if money:
                question = self.decision_one_money
            else:
                question = self.decision_one_without_money
            answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
            
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=self.survey.id)
            match.decisionOne()
            db.session.add(match)

    def _match_decision_two(self,list_users,money):
        for i in range(len(list_users)/2):
            print i, "of", len(list_users)/2, "decision two"
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            if money:
                question = self.decision_two_money
            else:
                question = self.decision_two_without_money

            answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=self.survey.id)
            match.decisionTwo()
            db.session.add(match)
    
    def _match_decision_three(self, list_users, money):
        for i in range(len(list_users)/2):
            print i, "of", len(list_users)/2, "decision trhee"
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            if money:
                question = self.decision_three_money
            else:
                question = self.decision_three_without_money

            answerA = Answer.query.filter_by(user_id=userA,question_id=question.id).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=question.id).first()
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=self.survey.id)
            match.decisionThree()
            db.session.add(match)

    def _match_decision_four(self, list_users, money):

        l=self._generate_tupla(list_users)
        if money:
            question_four = self.decision_four_money
            section_five = self.decision_five_money
        else:
            question_four = self.decision_four_without_money
            section_five = self.decision_five_without_money
        
        for i in range(len(l)):
            print i, "of", len(l), "decision four"

            answerA = Answer.query.filter_by(user_id=l[i][0],question_id=question_four.id).first()
            match = Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=self.survey.id)
            match.decisionFour(section_five.id)
            db.session.add(match)
    
    def _match_decision_six(self,list_users, money):

        l=self._generate_tupla(list_users)
        if money:
            question = self.decision_six_money
        else:
            question = self.decision_six_without_money

        for i in range(len(l)):
            print i, "of", len(l), "decision six"

            answerA = Answer.query.filter_by(user_id=l[i][0],question_id=question.id).first()
            match = Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=self.survey.id)
            match.decision_six()
            db.session.add(match)

    def _prize_decision_123(self,user,decision):
        match = Match.query.filter(\
            Match.survey==self.survey.id,\
            Match.type==decision,\
            or_(Match.userA==user, Match.userB==user)).first()
        if match.userA==user:
            match.prizeA=True
        elif match.userB==user:
            match.prizeB=True
        else:
            raise "error, user in decision one not found"
        db.session.add(match)

    def _prize_decision_4(self,user):
        match = Match.query.filter(\
            Match.survey==self.survey.id,\
            Match.type=="decision_four",\
            Match.userA==user).first()
        match.prizeA=True
        db.session.add(match)

    def _prize_decision_5(self,user):
        match = Match.query.filter(\
            Match.survey==self.survey.id,\
            Match.type=="decision_four",\
            Match.userB==user).first()
        match.prizeB=True
        db.session.add(match)

    def _prize_decision_6_playerA(self,user):
        match = Match.query.filter(\
            Match.survey==self.survey.id,\
            Match.type=="decision_six",\
            Match.userA==user).first()
        match.prizeA=True
        db.session.add(match)

    def _prize_decision_6_playerB(self,user):
        match = Match.query.filter(\
            Match.survey==self.survey.id,\
            Match.type=="decision_six",\
            Match.userB==user).first()
        match.prizeB=True
        db.session.add(match)

    def _prize(self,user):
        # can be implementated with dictionary, but lamba functions haven input parameters
        if random.randint(1,10)==1:
            #user prize
            n=random.randint(1,7)
            if n==1:
                self._prize_decision_123(user,"decision_one")
            elif n==2:
                self._prize_decision_123(user,"decision_two")
            elif n==3:
                self._prize_decision_123(user,"decision_three")
            elif n==4:
                self._prize_decision_4(user)
            elif n==5:
                self._prize_decision_5(user)
            elif n==6:
                self._prize_decision_6_playerA(user)
            elif n==7:
                self._prize_decision_6_playerB(user)

    
    def part_two(self,user):
        ans = Answer.query.filter(\
            Answer.user_id==user.id,\
            Answer.question_id==self.part_two_money[0]).first()
        if ans is not None:
            #game with real money
            question = random.choice(self.part_two_money)
            answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
            match = Match(userA=user.id, answerA = answer.id, survey=self.survey.id)
            state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
                StateSurvey.user_id==user.id).first()
            state_survey.status=state_survey.status | StateSurvey.PART_TWO_MONEY
            db.session.add(state_survey)
            db.session.commit()
            if random.randint(1,10)==1:
                #user prize
                match.prize=True
        else:
            question = random.choice(self.part_two_without_money)
            answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
            match = Match(userA=user.id, answerA = answer.id, survey=self.survey.id)
            state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
                StateSurvey.user_id==user.id).first()
            state_survey.status=state_survey.status | StateSurvey.PART_TWO_WITHOUT_MONEY

            db.session.add(state_survey)
            db.session.commit()
        match.part_two()
        db.session.add(match)
        db.session.commit()

    def matching(self):
        users_money=self._users_part_three_money()
        if len (users_money)>=self.MIN_USER_MATCH:
            l_aux=users_money[:]
            self._match_decision_one(l_aux, True)
            l_aux=users_money[:]
            self._match_decision_two(l_aux, True)
            l_aux=users_money[:]
            self._match_decision_three(l_aux, True)
            l_aux=users_money[:]
            self._match_decision_four(l_aux, True)
            l_aux=users_money[:]
            self._match_decision_six(l_aux, True)
            db.session.commit()
            for user in users_money:
                self._prize(user)
            db.session.commit()


        users_without_money=self._users_part_three_without_money()
        if len (users_money)>=self.MIN_USER_MATCH:
            l_aux=users_without_money[:]
            self._match_decision_one(l_aux, False)
            l_aux=users_without_money[:]
            self._match_decision_two(l_aux, False)
            l_aux=users_without_money[:]
            self._match_decision_three(l_aux, False)
            l_aux=users_without_money[:]
            self._match_decision_four(l_aux, False)
            l_aux=users_without_money[:]
            self._match_decision_six(l_aux, False)
            db.session.commit()
