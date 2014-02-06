from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField
from wtforms.validators import Required, Length

class PreguntaForm(Form):
    texto = TextAreaField('texto', validators = [Length(min = 1, max = 400)])
    obligatoriedad = BooleanField('obligatoriedad', default = True)

class PreguntaSeleccionForm(Form):
    #muestro 10 campos.. esto de puede mejorar de muchas formas, pero ahora vale
    #mejora: pasas una lista con los wtf, en views.py/seleccion algo de ajax y crear
    # campos, o javascript que oculto/muestro campos
    texto = TextAreaField('texto', validators = [Length(min = 1, max = 400)])
    texto1 = TextField('texto1', validators = [Length(min = 1, max = 400), Required])
    texto2 = TextField('texto2', validators = [Length(min = 1, max = 400), Required])
    texto3 = TextField('texto3', validators = [Length(min = 0, max = 400)])
    texto4 = TextField('texto4', validators = [Length(min = 0, max = 400)])
    texto5 = TextField('texto5', validators = [Length(min = 0, max = 400)])
    texto6 = TextField('texto6', validators = [Length(min = 0, max = 400)])
    texto7 = TextField('texto7', validators = [Length(min = 0, max = 400)])
    texto8 = TextField('texto8', validators = [Length(min = 0, max = 400)])
    texto9 = TextField('texto9', validators = [Length(min = 0, max = 400)])


class TipoPreguntaForm(Form):
    tipo = SelectField('tipo',choices=[('S/N','S/N'),('Numerica','Numerica'),('Texto','Texto'),('Seleccion','Seleccion')])
    #nCampos = IntegerField('nCampos')
