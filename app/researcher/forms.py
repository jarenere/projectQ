from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField, DecimalField, SubmitField, DateTimeField, FileField
from wtforms.validators import Required, Length, NumberRange, ValidationError, Optional
from flask.ext.pagedown import PageDown
from flask.ext.pagedown.fields import PageDownField



EXAMPLE_MARKDOWN = '## This is a example of Markdown\n**Markdown** is rendered on the fly in the <i>preview area</i>!\n\n\
More about [markdown](http://daringfireball.net/projects/markdown/).'

listQuestionType = [('yn', 'YES/NO'),('numerical','Numerical'),
        ('text','Text'),('choice','Choice'),('likertScale','Likert Scale'),
        ('partTwo','Part two'),('decisionOne','Decision One'),
        ('decisionTwo','Decision Two'),('decisionThree','Decision Three'),
        ('decisionFour','Decision Four'),('decisionFive','Decision Five'),
        ('decisionSix','Decision Six')]

class SurveyForm(Form):
    title = TextField('Title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('Description',validators = [Length(min = 0, max = 1200)],default = EXAMPLE_MARKDOWN)
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
    description = PageDownField('Description',validators = [Length(min = 0, max = 2200)],default = EXAMPLE_MARKDOWN)
    sequence = IntegerField('Sequence', validators = [NumberRange(min = 1)])
    # Field with two decimal, range 0-1
    percent = DecimalField ('Percent', validators = [NumberRange(min = 0, max = 1)],places=2, default=1)

class QuestionForm(Form):

    #: Text of the question
    text = PageDownField('Text',validators = [Length(min = 1)],default = EXAMPLE_MARKDOWN)
    #: If the question is obligatory or not
    required = BooleanField('Required', default = True)
    #: If time is register or not
    registerTime = BooleanField('Register time', default = False)
    #: Type of response
    questionType = SelectField('Type of question', choices=listQuestionType)

    #:dateValidation(text)
    isNumber = BooleanField('Number')
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
    answer1 = TextField('Answer 1', validators = [Length(min = 0, max =400)])
    answer2 = TextField('Answer 2', validators = [Length(min = 0, max =400)])
    answer3 = TextField('Answer 3', validators = [Length(min = 0, max =400)])
    answer4 = TextField('Answer 4', validators = [Length(min = 0, max =400)])
    answer5 = TextField('Answer 5', validators = [Length(min = 0, max =400)])
    answer6 = TextField('Answer 6', validators = [Length(min = 0, max =400)])
    answer7 = TextField('Answer 7', validators = [Length(min = 0, max =400)])
    answer8 = TextField('Answer 8', validators = [Length(min = 0, max =400)])
    answer9 = TextField('Answer 9', validators = [Length(min = 0, max =400)])

    def selectQuestionTypeDefault(self):
        self.questionType.default = 'Numerical'
        self.questionType.process()
        # self.questionType = SelectField('Type of question', choices=listQuestionType, default ='Numerical')
        # return self
        #     default = d)



    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        if not Form.validate(self):
            return False
        if self.questionType.data == 'choice':
            l = [self.answer1,
            self.answer2,
            self.answer3,
            self.answer4,
            self.answer5,
            self.answer6,
            self.answer7,
            self.answer8,
            self.answer9]
            state = False
            for i in  range (9):
                if len(l[i].data) != 0:
                    state = True
            if state ==False:
                l[0].errors.append('All field can not be empty')
            return state
        if self.questionType.data == 'partTwo':
            l = [self.answer1,
            self.answer2]
            state = True
            for i in  range (2):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state
        if self.questionType.data == 'decisionFive':
            l = [self.answer1]
            state = True
            for i in  range (1):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state

        return True
