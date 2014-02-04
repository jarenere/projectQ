from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField, DecimalField
from wtforms.validators import Required, Length, NumberRange


class EditSurveyForm(Form):
    title = TextField('title', validators = [Length(min = 1, max = 128)])
    description = TextAreaField('description',validators = [Length(min = 0, max = 1200)])

class EditConsentForm(Form):
    text = TextAreaField('text',validators = [Length(min = 1)])

class SectionForm(Form):
    title = TextField('title', validators = [Length(min = 1, max = 128)])
    description = TextAreaField('description',validators = [Length(min = 0, max = 1200)])
    sequence = IntegerField('sequence')
    # Field with two decimal, range 0-1
    percent = DecimalField ('percent', validators = [NumberRange(min = 0, max = 1)],places=2)