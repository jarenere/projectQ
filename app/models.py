# -*- coding: utf-8 -*-

from app import db


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
    numero = db.Column(db.Integer)
    #mmm.. almacenar en un json las posibles "respuestas" u
    #otra clase con las posibles respuestas.... va a ser que no
    campos = db.Column(db.String(400))


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
