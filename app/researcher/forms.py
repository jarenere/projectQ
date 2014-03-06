from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField, DecimalField, SubmitField, DateTimeField
from wtforms.validators import Required, Length, NumberRange, ValidationError, Optional
from flask.ext.pagedown import PageDown
from flask.ext.pagedown.fields import PageDownField



EXAMPLE_MARKDOWN = '## This is a example of Markdown\n**Markdown** is rendered on the fly in the <i>preview area</i>!\n\n\
More about [markdown](http://daringfireball.net/projects/markdown/).'

listQuestionType = [('YES/NO', 'YES/NO'),('Numerical','Numerical'),
        ('Text','Text'),('Choice','Choice'),('likert','Likert Scale'),
        ('PartTwo','Part two'),('DecisionOne','Decision One'),
        ('DecisionTwo','Decision Two'),('DecisionThree','Decision Three'),
        ('DecisionFour','Decision Four'),('DecisionFive','Decision Five'),
        ('DecisionSix','Decision Six')]

class SurveyForm(Form):
    title = TextField('Title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('Description',validators = [Length(min = 10, max = 1200)],default = EXAMPLE_MARKDOWN)
    startDate = DateTimeField('Day and start time', validators = [Optional()])
    endDate =DateTimeField('Day and finish time', validators = [Optional()])
    maxNumberRespondents = IntegerField('Number of respondents', validators = [Optional()])

#    submit = SubmitField('Register')


class EditConsentForm(Form):
    text = PageDownField('Consent',validators = [Length(min = 1)],default = EXAMPLE_MARKDOWN)

class SectionForm(Form):
    title = TextField('Title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('Sescription',validators = [Length(min = 0, max = 2200)],default = EXAMPLE_MARKDOWN)
    sequence = IntegerField('Sequence')
    # Field with two decimal, range 0-1
    percent = DecimalField ('Percent', validators = [NumberRange(min = 0, max = 1)],places=2)

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

    #: Number of fields in "choice question"
    numberFields = SelectField('number of fields in "choice question"',
        choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
        ('7','7'),('8','8'),('9','9')])
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
        if self.questionType.data == 'Choice':
            l = [self.answer1,
            self.answer2,
            self.answer3,
            self.answer4,
            self.answer5,
            self.answer6,
            self.answer7,
            self.answer8,
            self.answer9]
            state = True
            for i in  range (int(self.numberFields.data)):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state
        if self.questionType.data == 'PartTwo':
            l = [self.answer1,
            self.answer2]
            state = True
            for i in  range (2):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state
        if self.questionType.data == 'DecisionFive':
            l = [self.answer1]
            state = True
            for i in  range (1):
                if len(l[i].data) == 0:
                    l[i].errors.append('The field can not be empty')
                    state = False
            return state

        return True
