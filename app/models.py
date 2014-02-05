# -*- coding: utf-8 -*-

from app import db
import json
from datetime import datetime


class Survey(db.Model):
    '''A table with Survey
    '''
    #: unique id (automatically generated)
    id = db.Column(db.Integer, primary_key = True)
    #: Tittle for this Survey
    title = db.Column(db.String(128), nullable = False)
    #: description for this Survey
    description = db.Column(db.String(1200))
    #: created timestamp (automatically set)
    created = db.Column(db.DateTime, default = datetime.utcnow())
    ## Relationships
    #: Survey have zero or more consents
    consents = db.relationship('Consent', backref = 'survey', lazy = 'dynamic')
    #: Survey have zero or more sections 
    sections = db.relationship('Section', backref = 'survey', lazy = 'dynamic')



class Consent(db.Model):
    '''A table with Consents to a Survey
    '''
    #: unique id (automatically generated)
    id = db.Column(db.Integer, primary_key = True)
    #: Text for this consents
    text = db.Column(db.String, nullable = False)
    ## Relationships
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))

class Section(db.Model):
    '''A table with sections of a Survey
    '''
    #: unique id (automatically generated)
    id = db.Column(db.Integer, primary_key = True)
    #: Tittle for this section
    title = db.Column(db.String(128), nullable = False)
    #: description for this section
    description = db.Column(db.String)
    #: sequence of the section
    #If two or more sections of the same survey with the same sequence, 
    # is chosen at random which is done first
    sequence = db.Column(db.Integer, default = 1)
    #:Percentage of Respondents who pass through this section
    percent = db.Column(db.Numeric, default = 1)
    #: created timestamp (automatically set)
    created = db.Column(db.DateTime, default = datetime.utcnow())   
    ## Relationships
    #: section belongs to zero or more surveys 
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'))
    #: section belongs to zero or more sections
    parent_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    #: Section have zero or more subsections 
    #https://github.com/zzzeek/sqlalchemy/blob/master/examples/adjacency_list/adjacency_list.py
    #http://stackoverflow.com/questions/15044777/relating-a-class-to-its-self
    #distintas opciones, si queremos lazy dynamic debemos de forzar uselist
    #debido a a la relacion one to one, many to one
    #http://docs.sqlalchemy.org/en/rel_0_9/orm/relationships.html
    children = db.relationship('Section', 
        backref='section',remote_side=id, lazy = 'dynamic', uselist = True)




class Question(db.Model):
    #Clase Question
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(400))

    def __repr__(self):
        return '<Question %r>' % (self.id)

class QuestionNumber(Question):
    #Pregunta de tipo numero
    number = db.Column(db.Integer)

    def __repr__(self):
        return '<Question_numeber %r>' % (self.id)


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
