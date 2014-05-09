from flask.ext.wtf import Form
from flask.ext.babel import gettext
from wtforms import TextField, BooleanField, RadioField
from wtforms.validators import Required, Regexp, Optional
from wtforms import IntegerField, HiddenField
from wtforms import ValidationError
from wtforms.validators import StopValidation
from wtforms import SelectField
from app.models import Question, QuestionChoice, QuestionYN, QuestionText,Answer, QuestionLikertScale
from flask import g, flash
from app import db
from utiles import generate_answer


class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class LikertField(RadioField):
    '''my implement of likert field'''
    def __init__(self, label='', validators=None, labelMin="", labelMax="", **kwargs):
        self.labelMin=labelMin
        self.labelMax=labelMax
        super(LikertField, self).__init__(label, validators, **kwargs)

    def __call__(self, **kwargs):
        '''render likert as table
        '''
        from wtforms.widgets.core import html_params, HTMLString
        kwargs.setdefault('id', self.id)
        kwargs.setdefault('class_', " table table-condensed likert")
        html = ['<%s %s>' % ("table", html_params(**kwargs))]
        html.append('<tr>')
        html.append('<td></td>')
        for subfield in self:
            html.append('<td>%s</td>' % (subfield.label))
        html.append('</tr>')
        html.append('<tr>')
        html.append('<td class="type-info">%s</td>' % (self.labelMin))
        for subfield in self:
                html.append('<td>%s</td>' % (subfield()))
        html.append('<td class="type-info">%s</td>' % (self.labelMax))
        html.append('</tr>')

        html.append('</%s>' % "table")
        return  HTMLString(''.join(html))
        # return super(RadioFeild, self).__call__(**kwargs)

    def __call1__(self, **kwargs):
        '''render likert as list
        '''
        from wtforms.widgets.core import html_params, HTMLString
        kwargs.setdefault('id', self.id)
        kwargs.setdefault('class_', "likert")
        html = ['<%s %s>' % (self.widget.html_tag, html_params(**kwargs))]
        html.append('<li>%s</li>' % (self.labelMin))

        for subfield in self:
            if self.widget.prefix_label:
                html.append('<li>%s %s</li>' % (subfield.label, subfield()))
            else:
                html.append('<li>%s %s</li>' % (subfield(), subfield.label))
        html.append('<li>%s</li>' % (self.labelMax))
        html.append('</%s>' % self.widget.html_tag)
        return  HTMLString(''.join(html))
        # return super(RadioField, self).__call__(**kwargs)

class MyRadioField(RadioField):
    def __init__(self, label='', validators=None, horizontal=False,**kwargs):
        self.horizontal=horizontal
        # kwargs.setdefault('coerce', "int")
        super(MyRadioField, self).__init__(label, validators, **kwargs)

    def __call__(self, **kwargs):
        if self.horizontal:
            kwargs.setdefault('class_', "radioField_horizontal")
            self.widget.prefix_label=True
        else:
            kwargs.setdefault('class_', "radio")
            self.widget.prefix_label=False
        print "prefix: ",self.widget.prefix_label
        return super(MyRadioField, self).__call__(**kwargs)

class CheckAnswerExpected(object):
    '''check if the answer is the expected
    '''
    def __init__(self, message=None):
        if not message:
            self.message = gettext("wrong answer")
        else:  # pragma: no cover
            self.message = message

    def __call__(self, form, field):
        question = Question.query.get(field.name[1:])
        answer = generate_answer(question, form, g.user)
        db.session.add(answer)
        db.session.commit()
        if not answer.answerAttempt():
            if answer.isMoreAttempt():
                 raise ValidationError(self.message)
            else:
                flash(gettext("wrong answer, you can continue"))

class CheckSubquestion(object):
    '''check whether to answer the question or not
    '''
    def __call__(self, form, field):
        question = Question.query.get(field.name[1:])
        data = form["c"+str(question.parent.id)].data
        if isinstance (question.parent,QuestionYN):
            if data.lower()==question.condition.value.lower():
                pass
                # raise ValidationError('This field is required.')
            else:
                # nothing to check
                field.errors[:] = []
                raise StopValidation()
        if isinstance (question.parent,QuestionText) or \
            isinstance(question.parent,QuestionChoice):
            if question.condition.operation=="<":
                if data<question.condition.value:
                    pass
                else:
                    # nothing to check
                    field.errors[:] = []
                    raise StopValidation()
            if question.condition.operation=="==":
                if data==question.condition.value:
                    pass
                else:
                    # nothing to check
                    field.errors[:] = []
                    raise StopValidation()
            if question.condition.operation==">":
                if int(data)>int(question.condition.value):
                    pass
                else:
                    # nothing to check
                    field.errors[:] = []
                    raise StopValidation()

class RequiredSelectField(object):
    ''' check if there is answer
    '''
    def __init__(self, message=None):
        if not message:
            self.message = gettext("Option not valid")
        else:  # pragma: no cover
            self.message = message
    def __call__(self, form, field):
        if field.data=="":
            raise ValidationError(gettext("Option not valid"))



def check_answer_expected(self,field):
    '''check if the answer is the expected
        DEPRECATED!
    '''
    question = Question.query.get(field.name[1:])
    answer = Answer.query.filter(Answer.user_id==g.user.id,
            Answer.question_id==question.id).first()
    if answer is None:
        answer = Answer (answerText = field.data, user= g.user, question = question)
    else:
        answer.answerText = field.data
    answer.globalTime = self["globalTimec"+str(question.id)].data
    answer.differentialTime = self["differentialTimec"+str(question.id)].data
    db.session.add(answer)
    db.session.commit()
    if not answer.answerAttempt():
        if answer.isMoreAttempt():
            raise ValidationError(gettext("Wrong answer"))
        else:
            flash(gettext("wrong answer, you can continue"))

def check_answer_expected_yn(self,field):
    '''check if the answer is the expected
        DEPRECATED
    '''
    question = Question.query.get(field.name[1:])
    answer = Answer.query.filter(Answer.user_id==g.user.id,
            Answer.question_id==question.id).first()
    if answer is None:
        answer = Answer (answerYN = field.data=='Yes', user= g.user, question = question)
        answer.globalTime = self["globalTimec"+str(question.id)].data
        answer.differentialTime = self["differentialTimec"+str(question.id)].data
    else:
        answer.answerYN = field.data=='Yes'
        answer.answerText = str(answer.answerYN)
    db.session.add(answer)
    db.session.commit()
    if not answer.answerAttemptYN():
        if answer.isMoreAttempt():
            raise ValidationError(gettext("Wrong answer"))
        else:
            flash(gettext("wrong answer, you can continue"))

def check_subquestion(self,field):
    '''check whether to answer the question or not
        DEPRECATED
    '''
    question = Question.query.get(field.name[1:])
    data = self["c"+str(question.parent.id)].data
    if isinstance (question.parent,QuestionYN):
        if data.lower()==question.condition.value.lower():
            pass
            # raise ValidationError('This field is required.')
        else:
            # nothing to check
            field.errors[:] = []
            raise StopValidation()
    if isinstance (question.parent,QuestionText) or \
        isinstance(question.parent,QuestionChoice):
        if question.condition.operation=="<":
            if data<question.condition.value:
                pass
            else:
                # nothing to check
                field.errors[:] = []
                raise StopValidation()
        if question.condition.operation=="==":
            if data==question.condition.value:
                pass
            else:
                # nothing to check
                field.errors[:] = []
                raise StopValidation()
        if question.condition.operation==">":
            if int(data)>int(question.condition.value):
                pass
            else:
                # nothing to check
                field.errors[:] = []
                raise StopValidation()

def check_valid_select_field(self,field):
    # DEPRECATED
    if field.data=="":
        raise ValidationError(gettext("Option not valid"))

def generate_form(questions):
    '''dynamically generates the forms for surveys
    '''
    def frange(x, y, jump):
        '''implement of range to floats:
        '''
        while x < y:
            yield  '{0:g}'.format(float(x))
            x += jump

    class AnswerForm(Form):
        time = HiddenField('time',default=0)
        
    for question in questions:

        setattr(AnswerForm,"globalTimec"+str(question.id),HiddenField('globalTimec'+str(question.id),default=0))
        setattr(AnswerForm,"differentialTimec"+str(question.id),HiddenField('differentialTimec'+str(question.id),default=0))

        #added "c" to that the key is valid
        #First element must be a string, otherwise fail to valid choice

        if isinstance (question,QuestionYN):
            choices = [('Yes',gettext('Yes')),('No',gettext('No'))]
            if question.isSubquestion:
                setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer', 
                    choices = choices,validators = [CheckSubquestion()]))
            else:
                if question.isExpectedAnswer():
                    setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer', 
                        choices = choices, validators = [CheckAnswerExpected()]))
                elif question.required:
                    setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer', 
                        choices = choices,validators = [Required()]))
                else:
                    setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer', 
                        choices = choices,validators = [Optional()]))
        if isinstance (question,QuestionText):
            if question.isSubquestion:
                setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer',
                    validators = [CheckSubquestion()]))
            else:
                if question.required:
                    if question.regularExpression !="":
                        if question.isExpectedAnswer():
                            setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                                validators=[Required(), Regexp(question.regularExpression,0,question.errorMessage),
                                CheckAnswerExpected()]))
                        else:
                            setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                                validators=[Required(), Regexp(question.regularExpression,0,question.errorMessage)]))
                    elif question.isExpectedAnswer():
                        setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Required(),
                            CheckAnswerExpected()]))
                    elif question.isNumber:
                        setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer'))
                    else:
                        setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Required()]))
                else:
                    if question.regularExpression !="":
                        setattr(AnswerForm,"c"+str(question.id),TextField('Answer',
                            validators=[Optional(), Regexp(question.regularExpression,0,question.errorMessage)]))
                    elif question.isNumber:
                        setattr(AnswerForm,"c"+str(question.id),IntegerField('Answer',validators = [Optional()]))
                    else:
                        setattr(AnswerForm,"c"+str(question.id),TextField('Answer',validators = [Optional()]))
        if isinstance (question,QuestionChoice):
            if question.is_range:
                list = [(str(index),choice) for index,choice in enumerate(
                    frange(question.range_min,
                        question.range_max+question.range_step,
                        question.range_step))]
            else:
                list = [(str(index),choice) for index, choice in enumerate(question.choices)]
            if question.render == "select":
                list.insert(0,("",""))

            if question.isSubquestion:
                if question.render=="select":
                    setattr(AnswerForm,"c"+str(question.id),SelectField('Answer', 
                        choices = list,validators = [RequiredSelectField(),CheckSubquestion()]))
                else:
                    setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer',
                        horizontal=question.render=="horizontal",
                        choices = list,validators = [CheckSubquestion()]))
            else:
                if question.required:
                    if question.render =="select":
                        setattr(AnswerForm,"c"+str(question.id),SelectField('Answer', 
                            choices = list,validators = [RequiredSelectField()]))
                    else:
                        setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer', 
                            horizontal=question.render=="horizontal",
                            choices = list,validators = [Required()]))
                else:
                    if question.render =="select":
                        setattr(AnswerForm,"c"+str(question.id),SelectField('Answer', 
                            choices = list,validators = [RequiredSelectField()]))
                    else:
                        setattr(AnswerForm,"c"+str(question.id),MyRadioField('Answer',
                            horizontal=question.render=="horizontal",
                            choices = list,validators = [Optional()]))

        if isinstance (question, QuestionLikertScale):
            list = [(str(index),choice) for index,choice in enumerate(range(question.minLikert,question.maxLikert+1))]
            if question.required:
                setattr(AnswerForm,"c"+str(question.id),LikertField('Answer', 
                    choices = list,
                    labelMin= question.labelMin,
                    labelMax=question.labelMax,
                    validators = [Required()]))
            else:
                setattr(AnswerForm,"c"+str(question.id),RadioField('Answer', 
                    choices = list,validators = [Optional()]))
    form = AnswerForm()

    return form