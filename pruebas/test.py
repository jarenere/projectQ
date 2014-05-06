#!flask/bin/python
from app import db, models
nodo = models.Section(title="nodo raiz")
db.session.add(nodo)
db.session.commit()

nodo1 =models.Section(title="nodo 1",parent = nodo)
db.session.add(nodo1)
db.session.commit()

print "secciones"
nodos = models.Section.query.all()
for n in nodos:
  print n.id, n.parent_id, n.survey_id


print ""



nodo3 = models.Section(title="nodo3",parent = nodo)
db.session.add(nodo3)
db.session.commit()

nodo31 = models.Section(title="nodo31",parent =nodo3)
db.session.add(nodo31)
db.session.commit()




nodos = models.Section.query.all()
print "secciones"
for n in nodos:
  print n.id, n.parent_id
  

encuesta = models.Survey(title = "encuesta1")
db.session.add(encuesta)
db.session.commit()

consentimiento = models.Consent(text ="consentimiento1",survey = encuesta)
db.session.add(consentimiento)
db.session.commit()


consentimiento2 = models.Consent(text ="consentimiento2",survey = encuesta)
db.session.add(consentimiento2)
db.session.commit()

raiz_encuesta = models.Survey.query.get(1)
print ""
print raiz_encuesta.title

consentimientos = raiz_encuesta.consents
for c in consentimientos:
  print c.text





raiz = models.Section.query.get(1)
secciones = raiz.children

raiz_encuesta = models.Survey.query.get(1)
seccion = models.Section(title="hholaa", survey = raiz_encuesta)
db.session.add(seccion)
db.session.commit()

nodos = models.Section.query.all()
for n in nodos:
  print n.id, n.parent_id, n.survey_id
