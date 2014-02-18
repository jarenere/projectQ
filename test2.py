from app import db, models
from app.models import Section
import random

def  listar(sections):
    for s in sections:
        print "id", s.id, "sequecnia", s.sequence

def sequenceSectionsA(sections):
    '''Sections: are order by sequence
    #ss = models.Section.query.filter(models.Section.parent_id == 1).order_by(models.Section.sequence)
    generates the order in which sections are traversed
    '''
    iMin = 0
    lAux = []
    l2Aux= []
    if sections.count()==0:
        return []
    for index,section in enumerate(sections):
        if (sections[iMin].sequence!=section.sequence):
            #generamos una sublista aleatoria de elementos con la msima secuencia
            lAux.extend(random.sample(sections[iMin:index],index-iMin))
            iMin=index
    #caso para el ultimo tramo de elemento
    lAux.extend(random.sample(sections[iMin:sections.count()],sections.count()-iMin))
        #ya tenemos los "padres" ordenados aleatoriamente, ahora toca los hijos
    for section in lAux:
        l2Aux.append(section)
        l2Aux.extend(sequenceSectionsA(Section.query.filter(Section.parent_id==section.id).order_by(Section.sequence)))
    return l2Aux
