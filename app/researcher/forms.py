from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField, DecimalField, SubmitField, DateTimeField, FileField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import Required, Length, NumberRange, ValidationError, Optional
from flask.ext.pagedown import PageDown
from flask.ext.pagedown.fields import PageDownField
from app.models import User



EXAMPLE_MARKDOWN = '## This is a example of Markdown\n**Markdown** is rendered on the fly in the <i>preview area</i>!\n\n\
More about [markdown](http://daringfireball.net/projects/markdown/).'


class SurveyForm(Form):
    title = TextField('Title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('Description',validators = [Length(min = 0)],default = EXAMPLE_MARKDOWN)
    startDate = DateTimeField('Day and start time', validators = [Optional()])
    endDate =DateTimeField('Day and finish time', validators = [Optional()])
    maxNumberRespondents = IntegerField('Number of respondents', validators = [Optional()])
    duration = IntegerField('Time in minutes that a user has to answer the survey', validators = [Optional()])
    surveyXml = FileField("File survey xml", validators = [Optional()])
#    submit = SubmitField('Register')


class EditConsentForm(Form):
    text = PageDownField('Consent',validators = [Length(min = 1)],default = EXAMPLE_MARKDOWN)

class SectionForm(Form):
    title = TextField('Title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('Description',validators = [Length(min = 0)],default = EXAMPLE_MARKDOWN)
    sequence = IntegerField('Sequence', validators = [NumberRange(min = 1)])
    # Field with two decimal, range 0-1
    percent = DecimalField ('Percent', validators = [NumberRange(min = 0, max = 1)],places=2, default=1)

class QuestionForm(Form):
    listQuestionType = [('yn', 'YES/NO'),
            ('text','Text'),('choice','Choice'),('likertScale','Likert Scale')]
    listDecisions = [('none','None'),('part_two','Part two'),('decision_one_v1','Decision One v1'),
            ('decision_one_v2','Decision One v2'),('decision_two','Decision Two'),
            ('decision_three','Decision Three'),('decision_four','Decision Four'),
            ('decision_five','Decision Five'),('decision_six','Decision Six')]

    #: Text of the question
    text = PageDownField('Text',validators = [Length(min = 1)],default = EXAMPLE_MARKDOWN)
    #: If the question is obligatory or not
    required = BooleanField('Required', default = True)
    #: Type of response
    questionType = SelectField('Type of question', choices=listQuestionType, default="yn")
    #: Type of decisions
    decisionType = SelectField('Type of question', choices=listDecisions, default="none")


    #:dateValidation(text)
    isNumber = BooleanField('Number')
    isNumberFloat = BooleanField('Number Float')
    regularExpression = TextField('Regular Expression', validators = [Length(min=0, max=255)])
    errorMessage = TextField('Error Message', validators = [Length(min=0, max=255)])

    #:Expected Answer
    expectedAnswer = TextField('answer', validators = [Length(min = 0, max = 20)], 
        description='none if There isnt correct answer')
    maxNumberAttempt = IntegerField('Number of attempt', validators = [Optional()])

    #:is_money_real for part two and decision
    is_real_money = BooleanField('It is with money real', default = False)

    #likert Scale
    minLikert = SelectField('Scale',choices=[('0','0'),('1','1')], default=('1'))
    maxLikert = SelectField('to', choices=[('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
        ('7','7'),('8','8'),('9','9'),('10','10')], default=('7'))
    labelMinLikert= TextField('min', validators = [Length(min = 0, max = 128)], description = 'label optional')
    labelMaxLikert = TextField('max',validators = [Length(min = 0, max = 128)], description = 'label optional')

    #: text of possible answers of the choice questions
    range_min = IntegerField('Range min', validators = [Optional()])
    range_max = IntegerField('Range max', validators = [Optional()])
    answer1 = TextField('Answer 1', validators = [Length(min = 0, max =400)])
    answer2 = TextField('Answer 2', validators = [Length(min = 0, max =400)])
    answer3 = TextField('Answer 3', validators = [Length(min = 0, max =400)])
    answer4 = TextField('Answer 4', validators = [Length(min = 0, max =400)])
    answer5 = TextField('Answer 5', validators = [Length(min = 0, max =400)])
    answer6 = TextField('Answer 6', validators = [Length(min = 0, max =400)])
    answer7 = TextField('Answer 7', validators = [Length(min = 0, max =400)])
    answer8 = TextField('Answer 8', validators = [Length(min = 0, max =400)])
    answer9 = TextField('Answer 9', validators = [Length(min = 0, max =400)])
    answer10 = TextField('Answer 10', validators = [Length(min = 0, max =400)])

    #condition to that question depends on the answer to another question
    listOperations = [('none','None'),('<','<'),('==','='),('>','>')]
    operation = SelectField('Type of operation', choices=listOperations, default='none')
    value = TextField('Value', validators = [Length(min = 0, max =63)])
    question = QuerySelectField('Question',get_label='text',validators=[Optional()])




    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if self.decisionType.data == 'part_two':
            l = [self.answer1,
            self.answer2]
            state = True
            for i in  range (2):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state
        if self.decisionType.data == 'decision_five':
            l = [self.answer1]
            state = True
            for i in  range (1):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state
            
        if self.questionType.data == 'choice':

            l = [self.answer1,
            self.answer2,
            self.answer3,
            self.answer4,
            self.answer5,
            self.answer6,
            self.answer7,
            self.answer8,
            self.answer9,
            self.answer10]
            state = False
            for i in  range (9):
                if len(l[i].data) != 0:
                    state = True
            if state ==False:
                if (self.range_min.data is not None and self.range_max.data is not None):
                    if self.range_min.data<self.range_max.data:
                        state = True
                    else:
                        self.range_min.errors.append("Range min must be less than Range max")
                else:
                    l[0].errors.append('All field can not be empty')
            return state
        return True