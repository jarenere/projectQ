from app import db, models
from app.models import Section
import random

def  listar(sections):
    print ""
    print ""
    for s in sections:
        print "id", s.id, "titulo", s.title, "sequecnia", s.sequence, "percent", s.percent

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

def sequenceSectionsB(sections):
    '''Sections: are order by sequence
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
    
    #comprobamos el porcentaje de los que pasan por cada seccion, La suma del porcentaje
    #de todas las secciones (del mismo nivel y rama) deben sumar 1, si es 1 ignoramos
    ran =random.random()
    percent=0
    insert = False
    for index,section in enumerate(lAux):
        if section.percent!=1:
            percent = section.percent+percent
        #Si es uno, se deja
        if section.percent == 1:
            pass
        #Si el porcentaje es mayor que el aleatorio, se deja, el resto se borraran
        elif (percent >ran) and (not insert):
            insert = True
        else:
            del lAux[index]

    #ya tenemos los "padres" ordenados aleatoriamente, ahora toca los hijos
    for section in lAux:
        l2Aux.append(section)
        l2Aux.extend(sequenceSectionsB(Section.query.filter(
            Section.parent_id==section.id).order_by(Section.sequence)))
    return l2Aux