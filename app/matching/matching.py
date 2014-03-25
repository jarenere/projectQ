from app.models import StateSurvey, Answer, Section, Question, Match, User
import datetime
import random
from app import db, models


class Games:
    MIN_USER_MATCH = 6
    def __init__(self, survey):
        self.survey=survey
        self.part_two_money=self._find_part_two(True)
        self.part_two_without_money=self._find_part_two(False)
        self.decision_one_money=self._find_decision("decision_one",True)
        self.decision_one_without_money=self._decision("decision_one",False)
        self.decision_two_money=self._find_decision("decision_two",True)
        self.decision_two_without_money=self._decision("decision_two",False)
        self.decision_three_money=self._find_decision("decision_three",True)
        self.decision_three_without_money=self._decision("decision_three",False)
        self.decision_four_money=self._find_decision("decision_four",True)
        self.decision_four_without_money=self._decision("decision_four",False)
        self.decision_five_money=self._find_section_decision_five(True)
        self.decision_five_without_money=self._find_section_decision_five(False)
        self.decision_six_money=self._find_decision("decision_six",True)
        self.decision_six_without_money=self._decision("decision_six",False)

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
            Question.is_real_money==with_money).first()]
        return l
    
    def _users_part_three_money(self):
        state_surveys = StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==self.decision_one_money, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)
        l=[]
        if state_surveys.count()%2 == 0:
            for i in range(state_surveys.count()):
                l.append(state_surveys[i].user_id)
                # state_surveys[i].status=state_surveys[i].status | StateSurvey.MATCHING |\
                #     StateSurvey.PART_THREE_MONEY
                # db.session.add(state_surveys[i])
        else:
            # impar, last user out!
            for i in range(state_surveys.count()-1):
                l.append(state_surveys[i].user_id)
                # state_surveys[i].status=state_surveys[i].status | StateSurvey.MATCHING |\
                #     StateSurvey.PART_THREE_MONEY
                # db.session.add(state_surveys[i])
        return l

    def _users_part_three_without_money(self):
        state_surveys = StateSurvey.query.filter(\
            User.id==StateSurvey.user_id,\
            StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
            StateSurvey.survey_id==self.survey.id,\
            Question.id==self.decision_one_without_money, \
            Answer.question_id==Question.id,\
            Answer.user_id==User.id)
        l=[]
        if state_surveys.count()%2 == 0:
            for i in range(state_surveys.count()):
                l.append(state_surveys[i].user_id)
                state_surveys[i].status=state_surveys[i].status | StateSurvey.MATCHING
                db.session.add(state_surveys[i])
        else:
            # impar, last user out!
            for i in range(state_surveys.count()-1):
                l.append(state_surveys[i].user_id)
                state_surveys[i].status=state_surveys[i].status | StateSurvey.MATCHING
                db.session.add(state_surveys[i])
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
            section_five = self.decision_five_money
        
        for i in range(len(l)):
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
            answerA = Answer.query.filter_by(user_id=l[i][0],question_id=question.id).first()
            match = Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=self.survey.id)
            match.decision_six()
            db.session.add(match)

    
    def game_part_two(self,user):
        ans = Answer.query.filter(\
            Answer.user_id==user.id,\
            Answer.question_id==self.part_two_money[0]).first
        if ans is not None:
            #game with real money
            question = random.choice(self.part_two_money)
            answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
            match = Match(userA=user.id, answerA = answer.id, survey=self.survey.id)
            state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
                StateSurvey.user_id==user.id).first()
            state_survey.status==state_survey.status | StateSurvey.PART_TWO_MONEY
            db.session.add(state_survey)
            db.session.commit()
            if random.randint(1,10)==1:
                #user prize
                match.prize=True
        else:
            question = random.choice(self.part_two_without_money)
            answer = Answer.query.filter_by(user_id=user.id,question_id=question).first()
            match = Match(userA=user.id, answerA = answer.id, survey=self.survey.id)
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
            for user in users_money:
                state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
                    StateSurvey.user_id==user.id).fisrt()
                state_survey.status=state_survey.status | StateSurvey.MATCHING |\
                    StateSurvey.PART_THREE_MONEY
                db.session.add(state_survey)

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
            for user in users_money:
                state_survey=StateSurvey.query.filter(StateSurvey.survey_id==self.survey.id,\
                    StateSurvey.user_id==user.id).fisrt()
                state_survey.status=state_survey.status | StateSurvey.MATCHING
                db.session.add(state_survey)



def matching(survey):

    def generate_tupla(list_users):
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
    def match_decision_one(list_users):

        # pop two in two
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            # answerA =db.session.query(Answer.id).filter(Answer.question_id==49, Answer.user_id==2).first()
            answerA = Answer.query.filter_by(user_id=userA,question_id=DECISION_ONE).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=DECISION_ONE).first()
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionOne()
            db.session.add(match)

    def match_decision_two(list_users):
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            answerA = Answer.query.filter_by(user_id=userA,question_id=DECISION_TWO).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=DECISION_TWO).first()
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionTwo()
            db.session.add(match)

    def match_decision_three(list_users):
        for i in range(len(list_users)/2):
            userA = random.choice(list_users)
            list_users.remove(userA)
            userB = random.choice(list_users)
            list_users.remove(userB)
            answerA = Answer.query.filter_by(user_id=userA,question_id=DECISION_THREE).first()
            answerB = Answer.query.filter_by(user_id=userB,question_id=DECISION_THREE).first()
            match = Match(userA=userA, userB=userB,\
                answerA = answerA.id, answerB = answerB.id,\
                survey=survey.id)
            match.decisionThree()
            db.session.add(match)

    def match_decision_four(list_users):

        l=generate_tupla(list_users)
        for i in range(len(l)):
            answerA = Answer.query.filter_by(user_id=l[i][0],question_id=DECISION_FOUR).first()
            match = Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=survey.id)
            match.decisionFour(SECTION_DECISION_FIVE)
            db.session.add(match)

    def match_decision_six(list_users):

        l=generate_tupla(list_users)
        for i in range(len(l)):
            answerA = Answer.query.filter_by(user_id=l[i][0],question_id=DECISION_SIX).first()
            match = Match(userA=l[i][0], userB=l[i][1],\
                answerA = answerA.id,\
                survey=survey.id)
            match.decision_six()
            db.session.add(match)


    DECISION_ONE=47
    DECISION_TWO=48
    DECISION_THREE=49
    DECISION_FOUR=50
    SECTION_DECISION_FIVE=27
    DECISION_SIX=62
    # DEBEN SER PARES!! Y LOS USUARIOS SELECCIONADOS DEL MISMO GRUPO (PAGO Y NO PAGO)
    # users = User.query.filter(User.id==StateSurvey.user_id,\
    #      StateSurvey.status==StateSurvey.FINISH,\
    #      StateSurvey.survey_id==survey.id)
    state_surveys = StateSurvey.query.filter(User.id==StateSurvey.user_id,\
         StateSurvey.status.op('&')(StateSurvey.FINISH_OK),\
         StateSurvey.survey_id==survey.id)

    l=[]
    if state_surveys.count()%2 == 0:
        for i in range(state_surveys.count()):
            l.append(state_surveys[i].user_id)
            state_surveys[i].status=state_surveys[i].status & StateSurvey.MATCHING
            db.session.add(state_surveys[i])
    else:
        # impar, last user out!
        for i in range(state_surveys.count()-1):
            l.append(state_surveys[i].user_id)
            state_surveys[i].status=state_surveys[i].status & StateSurvey.MATCHING
            db.session.add(state_surveys[i])

    
    l_aux=l[:]
    match_decision_one(l_aux)

    l_aux=l[:]
    match_decision_two(l_aux)

    l_aux=l[:]
    match_decision_three(l_aux)

    l_aux=l[:]
    match_decision_four(l_aux)

    l_aux=l[:]
    match_decision_six(l_aux)

    db.session.commit()
