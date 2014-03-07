from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import xml.etree.cElementTree as ET
from app import db, models
from app.models import Section, Survey, Consent, Question, QuestionText, QuestionLikertScale

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