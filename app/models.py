# -*- coding: utf-8 -*-
from __future__ import division

from app import db
import json
import random
from datetime import datetime
from sqlalchemy import BigInteger, Integer, Boolean, Unicode,\
        Float, UnicodeText, Text, String, DateTime, Numeric, PickleType,\
        SmallInteger
from sqlalchemy.schema import Table, MetaData, Column, ForeignKey
from sqlalchemy.orm import relationship, backref, class_mapper
from sqlalchemy.types import TypeDecorator
from sqlalchemy import event, text
from sqlalchemy.engine import reflection
from sqlalchemy import create_engine
from sqlalchemy.orm.collections import attribute_mapped_collection

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.cElementTree as ET

class Survey(db.Model):
    '''A table with Survey
    '''
    __tablename__ = 'survey'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Tittle for this Survey
    title = Column(String(128), nullable = False)
    #: description for this Survey
    description = Column(String(1200))
    #: created timestamp (automatically set)
    created = Column(DateTime, default = datetime.utcnow())
    #: DateTime init survey
    startDate = Column(DateTime, default = datetime.utcnow())
    #: DateTime finish survey
    endDate = Column(DateTime, default = datetime.utcnow())
    #: max number of respondents, 0 is infinite
    maxNumberRespondents = Column(Integer, default = 0)
    ## Relationships
    #: Survey have zero or more consents
    consents = relationship('Consent',
        cascade="all, delete-orphan",
        backref = 'survey', lazy = 'dynamic')
    #: Survey have zero or more sections 
    sections = relationship('Section', 
        cascade="all, delete-orphan",
        backref = 'survey', lazy = 'dynamic')
    #: Survey have zero or more stateSurvey 
    stateSurveys = relationship('StateSurvey', backref = 'survey', lazy = 'dynamic')


    def to_json(self):
        json_survey = {
            'title': self.title,
            'description': self.description,
            'created': self.created,
            'startDate': self.startDate,
            'endDate': self.endDate,
            'maxNumberRespondents': self.maxNumberRespondents,
            # 'consents': self.consents.to_json(),
        }
        return json_survey

    def to_xml(self):
        '''write file:
        tree.write("output.xml",encoding="ISO-8859-1", method="xml")
        '''
        survey = Element('survey')
        title = SubElement(survey,'title')
        title.text = self.title

        description = SubElement(survey,'description')
        description.text = self.description
        
        startDate = SubElement(survey,'startDate')
        startDate.text = str(self.startDate)

        endDate = SubElement(survey,'endDate')
        endDate.text = str(self.endDate)

        maxNumberRespondents = SubElement(survey,'maxNumberRespondents')
        maxNumberRespondents.text = str(self.maxNumberRespondents)



        for consent in self.consents:
            #SubElement (consents,consentXml(consent))
            survey.append(consent.to_xml())


        for section in self.sections:
            survey.append(section.to_xml())

        tree = ET.ElementTree(survey)
        #tree = ET.ElementTree(consents)

        return tree




class Consent(db.Model):
    '''A table with Consents to a Survey
    '''
    __tablename__ = 'consent'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Text for this consents
    text = Column(String, nullable = False)
    ## Relationships
    survey_id = Column(Integer, ForeignKey('survey.id'))

    def to_json(self):
        json_survey = {
            'text': self.text,
        }
        return json_survey

    def to_xml(self):
        consent = Element('consent')
        consent.text = self.text
        return consent

class Section(db.Model):
    '''A table with sections of a Survey
    '''
    __tablename__ = 'section'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Tittle for this section
    title = Column(String(128), nullable = False)
    #: description for this section
    description = Column(String)
    #: sequence of the section
    #If two or more sections of the same survey with the same sequence, 
    # is chosen at random which is done first
    sequence = Column(Integer, default = 1)
    #:Percentage of Respondents who pass through this section
    percent = Column(Numeric, default = 1)
    #: created timestamp (automatically set)
    #created = Column(DateTime, default = datetime.utcnow())   
    
    ## Relationships
    #: Section have zero or more questions 
    questions = relationship('Question', 
        # cascade deletions
        cascade="all, delete-orphan",
        backref = 'section', lazy = 'dynamic')
    #: section belongs to zero or one surveys 
    survey_id = Column(Integer, ForeignKey('survey.id'))
    #: section belongs to zero or more sections
    parent_id = Column(Integer, ForeignKey(id))
    #: Section have zero or more subsections 
    #https://github.com/zzzeek/sqlalchemy/blob/master/examples/adjacency_list/adjacency_list.py
    #http://stackoverflow.com/questions/15044777/relating-a-class-to-its-self
    #distintas opciones, si queremos lazy dynamic debemos de forzar uselist
    #debido a a la relacion one to one, many to one
    #http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html
    # children = db.relationship('Section', 
    #     backref='section',remote_side=id, lazy = 'dynamic', uselist = True)
    #http://stackoverflow.com/questions/19606745/flask-sqlalchemy-error-typeerror-incompatible-collection-type-model-is-not
    # children = db.relationship('Section', 
    #     backref='parent',remote_side=id, lazy = 'dynamic',uselist = True,
    #     collection_class=attribute_mapped_collection('name')
    #     )
    # children = relationship('Section', backref=backref('parent', remote_side=id),
    #     collection_class=attribute_mapped_collection('name'))
    children = relationship('Section',
        # cascade deletions
        cascade="all, delete-orphan",
        backref=backref('parent', remote_side=id),
        lazy = 'dynamic', uselist = True)

    
    # def __init__(self, title, parent=None):
    #     self.title = title
    #     self.parent = parent


    def to_xml(self):
        section = Element('section')
        title = SubElement(section,'title')
        title.text = self.title
        
        description = SubElement(section,'description')
        description.text = self.description

        sequence = SubElement(section,'sequence')
        sequence.text = str(self.sequence)

        percent = SubElement(section,'percent')
        percent.text = str(self.percent)

        for question in self.questions:
             section.append(question.to_xml())


        for children in self.children:
            section.append(children.to_xml())

        return section

    @staticmethod
    def sequenceSections(sections):
        '''Sections: are order by sequence
        generates the order in which sections are traversed
        '''
        iMin = 0
        lAux = []
        l2Aux= []
        if sections.count()==0:
            return []
        for index,section in enumerate(sections):
            if (sections[iMin].sequence!=section.sequence):
                #generamos una sublista aleatoria de elementos con la msima secuencia
                lAux.extend(random.sample(sections[iMin:index],index-iMin))
                iMin=index
        #caso para el ultimo tramo de elemento
        lAux.extend(random.sample(sections[iMin:sections.count()],sections.count()-iMin))
        
        #comprobamos el porcentaje de los que pasan por cada seccion, La suma del porcentaje
        #de todas las secciones (del mismo nivel y rama) deben sumar 1, si es 1 ignoramos
        ran =random.random()
        percent=0
        insert = False
        for index,section in enumerate(lAux):
            if section.percent!=1:
                percent = section.percent+percent
            #Si es uno, se deja
            if section.percent == 1:
                pass
            #Si el porcentaje es mayor que el aleatorio, se deja, el resto se borraran
            elif (percent >ran) and (not insert):
                insert = True
            else:
                del lAux[index]


        #ya tenemos los "padres" ordenados aleatoriamente, ahora toca los hijos
        for section in lAux:
            l2Aux.append(section)
            l2Aux.extend(Section.sequenceSections(Section.query.filter(
                Section.parent_id==section.id).order_by(Section.sequence)))
        return l2Aux

class Question(db.Model):
    '''A table with Questions
    '''
    __tablename__ = 'question'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Text for this question
    text = Column(String, nullable = False)
    #: If the question is obligatory or not
    required = Column(Boolean, nullable = False)
    #: If time is register or not
    registerTime = Column(Boolean, nullable = False)
    #: possible choices
    choices = Column(PickleType)
    
    #: If there is a expected answer
    #expectedAnswer = Column(Boolean, default = False)
    #:expected answer
    expectedAnswer = Column(String(20))
    #:number of attempt to answer a question with  expected Answer
    # zero is infinite attempt to get the right answer
    numberAttempt = Column(Integer, default = 0)
    maxNumberAttempt = Column(Integer, default = 0)
    
    #: Type of question, discriminate between classes
    type = Column(String(20))
    __mapper_args__ = {'polymorphic_on': type}
    #: type2, two implementation, no classes
    type2 = Column(String(20))
    ## Relationships
    #: Question belong to one section
    section_id = Column(Integer, ForeignKey('section.id'))
    #: Question have zero or more answers
    answers = relationship('Answer', backref = 'question', lazy = 'dynamic')

    def isExpectedAnswer(self):
        '''return if there is a expected answer
        '''
        return len(self.expectedAnswer)>0

    def to_xml(self):
        question = Element('question')

        type = SubElement(question,'type')
        type.text = self.type

        text1 = SubElement(question,'text')
        text1.text = self.text

        required = SubElement(question,'required')
        required.text = str(self.required)

        if self.choices !=None:
            for choice in self.choices:
                c = SubElement(question,'choice')
                c.text = choice


        expectedAnswer = SubElement(question,'expectedAnswer')
        expectedAnswer.text = self.expectedAnswer

        maxNumberAttempt = SubElement(question,'maxNumberAttempt')
        maxNumberAttempt.text = self.maxNumberAttempt

        if isinstance (self, QuestionText):
            isNumber = SubElement(question,'isNumber')
            isNumber.text = str(self.isNumber)

            regularExpression = SubElement(question,'regularExpression')
            regularExpression.text = regularExpression.text

            errorMessage = SubElement(question,'errorMessage')
            errorMessage.text = self.errorMessage

        if isinstance (self, QuestionLikertScale):

            minLikert = SubElement(question,'minLikert')
            minLikert.text = str(self.minLikert)

            maxLikert = SubElement(question,'maxLikert')
            maxLikert.text = str(self.maxLikert)

            labelMin = SubElement(question,'labelMin')
            labelMin.text = self.labelMin

            labelMax = SubElement(question,'labelMax')
            labelMax.text = self.labelMax

        return question

class QuestionYN(Question):
    '''Question of type yes or no
    '''
    __mapper_args__ = {'polymorphic_identity': 'yn'}


class QuestionNumerical(Question):
    '''Question of type numerical
    '''
    __mapper_args__ = {'polymorphic_identity': 'numerical'}


class QuestionText(Question):
    '''Question of type text
    '''
    __mapper_args__ = {'polymorphic_identity': 'text'}
    isNumber = Column(Boolean, default=False)
    regularExpression = Column (String(256)) 
    #text with the error if the user answer with wrong  regular expression
    errorMessage = Column (String(256)) 

class QuestionChoice(Question):
    '''Question of type choice
    '''
    __mapper_args__ = {'polymorphic_identity': 'choice'}
    #: possible choices
    
    
    def number(self):
        return  len(self.choices)

class QuestionLikertScale(Question):
    '''Question of type likert Scale
    '''
    __mapper_args__ = {'polymorphic_identity': 'likertScale'}
    minLikert = Column(Integer)
    maxLikert = Column(Integer)
    labelMin = Column(String(128))
    labelMax = Column(String(128))



class QuestionPartTwo(Question):
    '''Question to part two, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'partTwo'}

    def len(self):
        return 2

class QuestionDecisionOne(Question):
    '''Question to part three, decision one, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionOne'}



class QuestionDecisionTwo(Question):
    '''Question to part three, decision two, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionTwo'}

class QuestionDecisionThree(Question):
    '''Question to part three, decision three, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionThree'}

class QuestionDecisionFour(Question):
    '''Question to part three, decision four, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionFour'}

class QuestionDecisionFive(Question):
    '''Question to part three, decision five, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionFive'}

    def len(self):
        return 1

    @staticmethod
    def getIntverval(section_id):
        '''return a list witch all interval
        '''
        l =[]
        for q in Section.query.get(section_id).questions:
            if isinstance (q, QuestionDecisionFive):
                l.append((q.choices[0],q.id))
        return l


class QuestionDecisionSix(Question):
    '''Question to part three, decision six, addoc
    '''
    __mapper_args__ = {'polymorphic_identity': 'decisionSix'}




    



class Match(db.Model):
    '''stores the results of the decisions depend on more than one user
    '''

    __tablename__ = 'match'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: user A
    userA = Column(Integer, ForeignKey('user.id'))
    #:user B
    userB = Column(Integer, ForeignKey('user.id'))
    #:answer  of User A
    answerA = Column(Integer, ForeignKey('answer.id'))
    #:answer of User B
    answerB = Column(Integer, ForeignKey('answer.id'))
    #:type of decision, each decisision have a different algorithm
    type = Column(String(20))
    #:user win
    win = Column(Integer,ForeignKey('user.id'))
    #:money earned of userA
    moneyA = Column(Numeric)
    #:money earned of userB
    moneyB = Column(Numeric)

    @staticmethod
    def Matching():
        '''search user/answer that no Matching with other user/answer
        '''
        pass

    def cashInitA(self):
        return Answer.query.get(self.answerA).answerNumeric

    def cashInitB(self):
        return Answer.query.get(self.answerB).answerNumeric


    def decisionOne(self):
        '''Probability:= userA_Money/(userA_Money+user_MoneyB)
        '''

        AWARD = 10
        INIT_MONEY = 10
        
        self.type = 'decisionOne'
        percentA=self.cashInitA()/(self.cashInitA()+self.cashInitB())
        if percentA>random.random():
            #answerA win
            self.win = self.userA
            self.moneyA = AWARD + (INIT_MONEY - self.cashInitA())
            self.moneyB = (INIT_MONEY - self.cashInitB())
        else:
            self.win = self.userB
            self.moneyB = AWARD + (INIT_MONEY - self.cashInitB())
            self.moneyA = (INIT_MONEY - self.cashInitA())
        print "ganador:", self.win
        print "percentA", percentA
        print "dinero jugadorA:", self.moneyA
        print "dinero jugadorB:", self.moneyB


    def decisionTwo(self):
        INIT_MONEY = 10
        CONSTANT_FUND = 0.8
        fund = (self.cashInitA()+self.cashInitB())*CONSTANT_FUND
        self.moneyA = fund + INIT_MONEY - self.cashInitA()
        self.moneyB = fund + INIT_MONEY - self.cashInitB()
        print "initA", self.cashInitA()
        print "initB", self.cashInitB()
        print "fondo", fund
        print "moneyA", self.moneyA
        print "moneyB", self.moneyB

    def decisionThree(self):
        INIT_MONEY = 10
        CONSTANT_FUND = 1.2
        fund = (self.cashInitA()+self.cashInitB())*CONSTANT_FUND
        self.moneyA = fund + INIT_MONEY - self.cashInitA()
        self.moneyB = fund + INIT_MONEY - self.cashInitB()
        print "initA", self.cashInitA()
        print "initB", self.cashInitB()
        print "fondo", fund
        print "moneyA", self.moneyA
        print "moneyB", self.moneyB

    def decisionFour(self, section_id):
        '''userB decision to accept o refuse, section_id is where store question type decisisonfive
            if userA win, the userB have accepted the money
        '''
        MONEY = 20
        interval = QuestionDecisionFive.getIntverval(section_id)
        for i in interval:
            if int(i[0])==self.cashInitA():
            #in i[1] if of question
                answer = Answer.query.filter(Answer.question_id == i[1],Answer.user_id == self.userB).first()
                if answer.answerYN:
                    self.win = self.userA
                    self.moneyA = MONEY - self.cashInitA()
                    self.moneyB = self.cashInitA()
                else:
                    self.win = self.userB
                    self.moneyA = 0
                    self.moneyB = 0
                print "win", self.win
                print "initA", self.cashInitA()
                #print "initB", self.cashInitB()
                print "moneyA", self.moneyA
                print "moneyB", self.moneyB
                return
        



  #          stateSurvey = StateSurvey.query.filter(StateSurvey.survey_id == id_survey, 
  #               StateSurvey.user_id == user.id).first()


    def decisionFourAcpet(self):
        '''return if userB accept the division of money
        '''
        return self.win ==self.userA



ROLE_USER = 0
ROLE_RESEARCHER = 1
ROLE_ADMIN = 2


class User(db.Model):
    '''A table with user
    '''
    __tablename__ = 'user'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: created timestamp (automatically set)
    created = Column(DateTime, default = datetime.utcnow())
    #: email address ...
    email = Column(Unicode(length=254), unique=True, nullable=False)
    #: user name
    nickname = Column(String(64), unique = True)
    #: role of user
    role = Column(SmallInteger, default = ROLE_USER)
    ## Relationships
    #: User have zero or more answers
    answers = relationship('Answer', backref = 'user', lazy = 'dynamic')
    #: User have zero or more stateSurvey
    stateSurveys = relationship('StateSurvey', backref = 'user', lazy = 'dynamic')

    def is_authenticated(self):
        '''Returns True if the user is authenticated, i.e. they have provided 
        valid credentials. (Only authenticated users will fulfill the criteria 
        of login_required.)
        '''
        return True

    def is_active(self):
        '''Returns True if this is an active user - in addition to being
        authenticated, they also have activated their account, not been
        suspended, or any condition your application has for rejecting an
        account. Inactive accounts may not log in (without being forced of
        course).
        '''
        return True

    def is_anonymous(self):
        '''Returns True if this is an anonymous user. (Actual users should 
        return False instead.)
        '''
        return False

    def get_id(self):
        '''Returns a unicode that uniquely identifies this user, and can be
        used to load the user from the user_loader callback. Note that this 
        must be a unicode 
        '''
        return unicode(self.id)



class Answer(db.Model):
    '''A table with answers
    '''
    __tablename__ = 'answer'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: created timestamp (automatically set)
    created = Column(DateTime, default = datetime.utcnow())
    #: answer Numeric
    answerNumeric = Column(Integer)
    #: answer Text
    answerText = Column(String)
    #: answer Boolean
    answerYN = Column(Boolean)
    #:numberAttemp do in a question with expected answer
    numberAttempt = Column(Integer, default = 1)
    ## Relationships
    #answer belong a user
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #answer belong a question
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)

    def answerAttempt(self):
        '''Return if the answer is the correct, else increment in 1
        the number attempt
        '''
        if self.question.isExpectedAnswer():
            if self.answerText.lower() != self.question.expectedAnswer.lower():
                self.numberAttempt = self.numberAttempt + 1
                db.session.add(self)
                db.session.commit()
                return False
            else:
                return True
        else:               
            return True

    def isMoreAttempt(self):
        '''Return if there are more attempt
        '''
        if self.numberAttempt>=self.question.maxNumberAttempt:
            return False
        else:
            return True

class StateSurvey(db.Model):
    '''A table that saves the state of a survey  
    '''
    __tablename__ = 'stateSurvey'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: created timestamp (automatically set)
    created = Column(DateTime, default = datetime.utcnow())
    #: Consent accept or not
    consented = Column(Boolean, default=False)
    #: finished or not
    finish = Column(Boolean, default =False)
    #: Sequence of sections are traversed (it is a list of secction to go through )
    sequence = Column(PickleType)
    #: index the lastt sections made
    index = Column(Integer, default =0)
    ## Relationships
    #stateSurvey belong a user
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #stateSurvey belong a survey
    survey_id = Column(Integer, ForeignKey('survey.id'), nullable=False)
    
    def nextSection(self):
        '''Return next Section to do
        '''
        # if self.index>=len(self.sequence):
        #     return None
        # else:
        #     return self.sequence[self.index]

        if self.index>=len(self.sequence):
            return None
        section = self.sequence[self.index]
        #section.questions.count always return 0, rare rare rare
        s = Section.query.get(section.id)
        if ((len(section.description)==0) and (s.questions.count()==0)):
            self.finishedSection()
            return self.nextSection()
        else:
            print s.questions
            print "___________________"
            print section.questions
            return section


    def isFinished(self):
        '''return there isn't more sections to do
        '''
        return self.index>=len(self.sequence)

        
    def finishedSection(self):
        '''Section is finished, index+1
        '''
        self.index=self.index+1
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getStateSurvey(id_survey, user):
        stateSurvey = StateSurvey.query.filter(StateSurvey.survey_id == id_survey, 
            StateSurvey.user_id == user.id).first()
        if stateSurvey is None:
            #generamos arbol
            ss = Section.query.filter(Section.survey_id == id_survey).order_by(Section.sequence)
            list = Section.sequenceSections(ss)

            stateSurvey = StateSurvey(survey = Survey.query.get(id_survey),
            user = user, sequence =list)
            db.session.add(stateSurvey)
            db.session.commit()  
        return stateSurvey




# class Question(db.Model):
#     #Clase Question
#     id = db.Column(db.Integer, primary_key = True)
#     text = db.Column(db.String(400))

#     def __repr__(self):
#         return '<Question %r>' % (self.id)

# class QuestionNumber(Question):
#     #Pregunta de tipo numero
#     number = db.Column(db.Integer)

#     def __repr__(self):
#         return '<Question_numeber %r>' % (self.id)


class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    texto = db.Column(db.String(400))
    obligatoriedad = db.Column(db.Boolean)
    discriminador = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminador}

class PreguntaNumerica(Pregunta):
    __mapper_args__ = {'polymorphic_identity': 'numerica'}

class PreguntaTexto(Pregunta):
    __mapper_args__ = {'polymorphic_identity' : 'texto'}

class PreguntaSeleccion(Pregunta):
    __mapper_args__ = {'polymorphic_identity' : 'seleccion'}
    #mmm.. almacenar en una picke las posibles "respuestas" u
    #otra clase con las posibles respuestas.... va a ser que no
    opciones = db.Column(db.PickleType)

    def numero(self):
        return  len(self.opciones)

class PreguntaSN(Pregunta):
    __mapper_args__ = {'polymorphic_identity' : 's/n'}




class Respuesta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.DateTime)
    Usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    discriminador = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminador}

class RespuestaNumerica(Respuesta):
    __mapper_args__ = {'polymorphic_identity': 'numerica'}
    respuestaNumerica = db.Column(db.Integer)

class RespuestaTexto(Respuesta):
    __mapper_args__ = {'polymorphic_identity': 'texto'}
    respuestaTexto = db.Column(db.String(64))

class RespuestaSeleccion(Respuesta):
    #habrá que comprobar que el rango de la respuesta es correcta
    __mapper_args__ = {'polymorphic_identity': 'seleccion'}
    respuestaSeleccion = db.Column(db.Integer)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64))
    respuestas = db.relationship('Respuesta', backref = 'autor', lazy = 'dynamic')
