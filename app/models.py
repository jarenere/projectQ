# -*- coding: utf-8 -*-

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
    ## Relationships
    #: Survey have zero or more consents
    consents = relationship('Consent', backref = 'survey', lazy = 'dynamic')
    #: Survey have zero or more sections 
    sections = relationship('Section', backref = 'survey', lazy = 'dynamic')
    #: Survey have zero or more stateSurvey 
    stateSurveys = relationship('StateSurvey', backref = 'survey', lazy = 'dynamic')




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
    #: Type of question, discriminate between classes
    type = Column(String(20))
    __mapper_args__ = {'polymorphic_on': type}
    ## Relationships
    #: Question belong to one section
    section_id = Column(Integer, ForeignKey('section.id'))
    #: Question have zero or more answers
    answers = relationship('Answer', backref = 'question', lazy = 'dynamic')


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

class QuestionChoice(Question):
    '''Question of type choice
    '''
    __mapper_args__ = {'polymorphic_identity': 'choice'}
    #: possible choices
    choices = Column(PickleType)
    
    def number(self):
        return  len(self.choices)


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
    ## Relationships
    #answer belong a user
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    #answer belong a question
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)

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
        if self.index>=len(self.sequence):
            return None
        else:
            return self.sequence[self.index]

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
