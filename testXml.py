from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.cElementTree as ET
from app import db, models
from app.models import Section, Survey, Consent, Question, QuestionText, QuestionLikertScale,\
    QuestionYN, QuestionNumerical, QuestionChoice, QuestionPartTwo, QuestionDecisionOne, \
    QuestionDecisionThree, QuestionDecisionThree, QuestionDecisionFour, QuestionDecisionFive, \
    QuestionDecisionTwo, QuestionDecisionSix

def surveyXml(surveyData):
    survey = Element('survey')
    title = SubElement(survey,'title')
    title.text = surveyData.title

    description = SubElement(survey,'description')
    description.text = surveyData.description
    
    startDate = SubElement(survey,'startDate')
    startDate.text = str(surveyData.startDate)

    endDate = SubElement(survey,'endDate')
    endDate.text = str(surveyData.endDate)

    maxNumberRespondents = SubElement(survey,'maxNumberRespondents')
    maxNumberRespondents.text = str(surveyData.maxNumberRespondents)


    consents = Element('consents')

    for consent in surveyData.consents:
        #SubElement (consents,consentXml(consent))
        consents.append(consentXml(consent))

    survey.append(consents)

    for s in surveyData.sections:
        survey.append(sectionXml(s))

    tree = ET.ElementTree(survey)
    #tree = ET.ElementTree(consents)

    return tree

def consentXml(consentData):
    consent = Element('consent')
    consent.text = consentData.text
    return consent

def sectionXml(sectionData):
    section = Element('section')
    title = SubElement(section,'title')
    title.text = sectionData.title
    
    description = SubElement(section,'description')
    description.text = sectionData.description

    sequence = SubElement(section,'sequence')
    sequence.text = str(sectionData.sequence)

    percent = SubElement(section,'percent')
    percent.text = str(sectionData.percent)

    for q in sectionData.questions:
         section.append(questionXml(q))


    for s in sectionData.children:
        section.append(sectionXml(s))

    return section

def questionXml(questionData):
    question = Element('question')

    type = SubElement(question,'type')
    type.text = questionData.type

    text = SubElement(question,'text')
    text.text = questionData.text

    required = SubElement(question,'required')
    required.text = str(questionData.required)

    if questionData.choices !=None:
        for choice in questionData.choices:
            c = SubElement(question,'choice')
            c.text = choice


    expectedAnswer = SubElement(question,'expectedAnswer')
    expectedAnswer.text = questionData.expectedAnswer

    maxNumberAttempt = SubElement(question,'maxNumberAttempt')
    maxNumberAttempt.text = questionData.maxNumberAttempt

    if isinstance (questionData, QuestionText):
        isNumber = SubElement(question,'isNumber')
        isNumber.text = str(questionData.isNumber)

        regularExpression = SubElement(question,'regularExpression')
        regularExpression.text = regularExpression.text

        errorMessage = SubElement(question,'errorMessage')
        errorMessage.text = questionData.errorMessage

    if isinstance (questionData, QuestionLikertScale):

        minLikert = SubElement(question,'minLikert')
        minLikert.text = str(questionData.minLikert)

        maxLikert = SubElement(question,'maxLikert')
        maxLikert.text = str(questionData.maxLikert)

        labelMin = SubElement(question,'labelMin')
        labelMin.text = questionData.labelMin

        labelMax = SubElement(question,'labelMax')
        labelMax.text = questionData.labelMax

    return question


def verSurvey(survey):
    print "title",survey.title
    print "description", survey.description
    print "startDate", survey.startDate
    print "endDate", survey.endDate
    print "maxNumberRespondents", survey.maxNumberRespondents


# def findField(str, root, msg = None):
#     try:
#         field=root.find(str).text
#         if field == "None":
#             #WTF!! return str "None" instead of NoneType
#             return None
#         return field
#     except:
#         if msg !=None :
#             msg.append(str + " not found")
#         return None

def findField(str, root, msg = None):
    try:
        field=root.find(str).text
        return field
    except:
        if msg !=None :
            msg.append(str + " not found")
        return None

def fromXmlQuestion(root,section,msg):
    text = findField('text',root,msg)
    required = (findField('required',root,msg) =="True")

    #CHOICES = findField('sequence',root,msg)
    l=[]
    for choice in root.findall('choice'):
        l.append(choice.text)

    expectedAnswer = findField('expectedAnswer',root,msg)
    maxNumberAttempt = findField('maxNumberAttempt',root,msg)
    type = findField('type',root,msg)
    
    if type == 'yn':
        question = QuestionYN()
    
    elif type == 'numerical':
        question = QuestionNumerical()

    elif type == 'text':
        isNumber = (findField('isNumber',root,msg)=="True")
        regularExpression = findField('regularExpression',root,msg)
        errorMessage = findField('errorMessage',root,msg)
        question = QuestionText(isNumber=isNumber,
            regularExpression=regularExpression,
            errorMessage=errorMessage)

    elif type == 'choice':
        question = QuestionChoice()

    elif type == 'likertScale':
        minLikert = findField('minLikert',root,msg)
        maxLikert = findField('maxLikert',root,msg)
        labelMin = findField('labelMin',root,msg)
        labelMax = findField('labelMax',root,msg)
        question = QuestionLikertScale(minLikert=minLikert,
            maxLikert=maxLikert,
            labelMin=labelMin,
            labelMax=labelMax)


    elif type == 'partTwo':
        question = QuestionPartTwo()

    elif type == 'decisionOne':
        question = QuestionDecisionOne()


    elif type == 'decisionTwo':
        question = QuestionDecisionTwo()

    elif type == 'decisionThree':
        question = QuestionDecisionThree()

    elif type == 'decisionFour':
        question = QuestionDecisionFour()

    elif type == 'decisionFive':
        question = QuestionDecisionFive()
    elif type == 'decisionSix':
        question = QuestionDecisionSix()
    else:
        print "MIERDA, typo:", type
        print "mierta texto: ", text
        return False

    question.text = text
    question.required = required
    question.expectedAnswer = expectedAnswer
    question.maxNumberAttempt = maxNumberAttempt
    question.choices = l
    question.section = section
    question.registerTime = False
    
    db.session.add(question)








def fromXmlSubSection(root,parent,msg):

    title = findField('title',root,msg)
    description = findField('description',root,msg)
    sequence = findField('sequence',root,msg)
    percent = findField('percent',root,msg)

    section = models.Section(title = title,
        description = description,
        sequence = sequence,
        percent = percent,
        parent = parent
        )
    db.session.add(section)

    for q in root.findall('question'):
        fromXmlQuestion(q, section, msg)

    for s in root.findall('section'):
        fromXmlSubSection(s,section,msg)





def fromXmlSection(root,survey,msg):
    title = findField('title',root,msg)
    description = findField('description',root,msg)
    sequence = findField('sequence',root,msg)
    percent = findField('percent',root,msg)

    section = models.Section(title = title,
        description = description,
        sequence = sequence,
        percent = percent,
        survey = survey
        )
    db.session.add(section)

    for q in root.findall('question'):
        fromXmlQuestion(q, section, msg)

    for s in root.findall('section'):
        fromXmlSubSection(s,section,msg)

def fromXmlConsent(cons, survey):
    consent = models.Consent(text = cons.text, 
            survey = survey)
    db.session.add(consent)




def fromxmlsurvey():
    '''
    MIRAR LOS TIPOS DE DATOS NONETYPE Y NONE, CUANDO CREO EL RECORRIDO PETA POR ALGUNA SECCION NONETYPE EN VEZ DE VACIA
    LINEA 702 CREO
    '''

    root = ET.parse('output.xml')
    msg = []

    title = findField('title',root,msg)
    description = findField('description',root,msg)
    startDate = findField('startDate',root,msg)
    endDate = findField('endDate',root,msg)
    maxNumberRespondents = findField('maxNumberRespondents',root,msg)
    # print "startDate: ", type(startDate), "v/F:", startDate ==None

    # print "startDate2: ", startDate2, "v/F:", startDate2 ==None

    # print "startDate3: ", startDate2, "v/F:", startDate == startDate2

    # print "startDate4: ", startDate2, "v/F:", startDate == "None"



    survey = models.Survey(title = title, description = description,
        startDate = startDate, endDate = endDate,
        maxNumberRespondents = maxNumberRespondents)


    # print ("SURVEY:")
    # verSurvey(survey)


    db.session.add(survey)


    for co in root.findall('consent'):
        consent = models.Consent(text = co.text, 
            survey = survey)
        db.session.add(consent)

    for co in root.findall('consent'):
        fromXmlConsent(consent,survey)

    for section in root.findall('section'):
        fromXmlSection(section,survey,msg)

    db.session.commit()
    # try:
    #     db.session.commit()
    # except :
    #     print "MIERDAAAAA"
    #     db.session.rollback()





    
    print ("ERRORES:")
    for m in msg:
        print m

