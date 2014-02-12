from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, RadioField, SelectField, IntegerField, TextAreaField, TextField, DecimalField
from wtforms.validators import Required, Length, NumberRange, ValidationError
from flask.ext.pagedown import PageDown
from flask.ext.pagedown.fields import PageDownField

EXAMPLE_MARKDOWN = '## This is a example of Markdown\n**Markdown** is rendered on the fly in the <i>preview area</i>!\n\n\
More about [markdown](http://daringfireball.net/projects/markdown/).'

class SurveyForm(Form):
    title = TextField('title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('description',validators = [Length(min = 10, max = 1200)],default = EXAMPLE_MARKDOWN)

class EditConsentForm(Form):
    text = PageDownField('text',validators = [Length(min = 1)],default = EXAMPLE_MARKDOWN)

class SectionForm(Form):
    title = TextField('title', validators = [Length(min = 1, max = 128)])
    description = PageDownField('description',validators = [Length(min = 0, max = 1200)],default = EXAMPLE_MARKDOWN)
    sequence = IntegerField('sequence')
    # Field with two decimal, range 0-1
    percent = DecimalField ('percent', validators = [NumberRange(min = 0, max = 1)],places=2)

class QuestionForm(Form):
    #: Text of the question
    text = TextAreaField('text',validators = [Length(min = 1)])
    #: If the question is obligatory or not
    required = BooleanField('required', default = True)
    #: If time is register or not
    registerTime = BooleanField('required', default = False)
    #: Type of response
    questionType = SelectField('question type', choices=[('YES/NO', 'YES/NO'),
        ('Numerical','Numerical'),('Text','Text'),('Choice','Choice')])
    #: Number of fields in "choice question"
    numberFields = SelectField('number of fields in choice question',
        choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),
        ('7','7'),('8','8'),('9','9')])
    #: text of possible answers of the choice questions
    answer1 = TextField('answer 1', validators = [Length(min = 0, max =400)])
    answer2 = TextField('answer 2', validators = [Length(min = 0, max =400)])
    answer3 = TextField('answer 3', validators = [Length(min = 0, max =400)])
    answer4 = TextField('answer 4', validators = [Length(min = 0, max =400)])
    answer5 = TextField('answer 5', validators = [Length(min = 0, max =400)])
    answer6 = TextField('answer 6', validators = [Length(min = 0, max =400)])
    answer7 = TextField('answer 7', validators = [Length(min = 0, max =400)])
    answer8 = TextField('answer 8', validators = [Length(min = 0, max =400)])
    answer9 = TextField('answer 9', validators = [Length(min = 0, max =400)])


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
        return True
