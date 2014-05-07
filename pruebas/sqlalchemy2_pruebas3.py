from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, relationship, backref,\
                                joinedload_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.schema import UniqueConstraint



Base = declarative_base()


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  address_id = Column(Integer,ForeignKey('address.id'))
  j = Column(Integer)
  __table_args__ = (UniqueConstraint('address_id', 'j'),)
  address = relationship("Address")
  def __repr__(self):
    return "<User(i='%s', j='%s')>" % (
      self.address_id, self.j)

class Address(Base):
  __tablename__ = 'address'
  id = Column(Integer, primary_key=True)
  def __repr__(self):
    return "<addres(i='%s')>" % (self.id)

engine = create_engine('sqlite://', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


ad1= Address()
session.add(ad1)


--------
u1=User(i=1,j=1)
session.add(u1)
u2=User(i=2,j=2)
session.add(u2)
session.commit()
u3=User(i=2,j=2)
session.add(u3)
session.commit()





for u, a in session.query(User, Address).\
  filter(User.id==Address.user_id).\
  filter(Address.email_address=='user1@').\
  all():   
  print u
  print a


stmt = db.session.query(models.StateSurvey.survey_id, models.StateSurvey.status).filter(models.StateSurvey.user_id==1).subquery()

for survey, status in db.session.query(models.Survey, stmt.c.status).outerjoin(stmt,models.Survey.id==stmt.c.survey_id): print survey, status

stmt2 = db.session.query(models.StateSurvey.survey_id, func.count('*').label('respondents_count')).group_by(models.StateSurvey.survey_id).subquery()



for survey, count in db.session.query(models.Survey, stmt2.c.respondents_count).outerjoin(stmt2,models.Survey.id==stmt2.c.survey_id): print survey, count


for survey, status, count  in db.session.query(models.Survey, stmt.c.status, stmt2.c.respondents_count).outerjoin(stmt,models.Survey.id==stmt.c.survey_id).outerjoin(stmt2,models.Survey.id==stmt2.c.survey_id): print survey, status, count

surveys = db.session.query(models.Survey, stmt.c.status, stmt2.c.respondents_count).outerjoin(stmt,models.Survey.id==stmt.c.survey_id).outerjoin(stmt2,models.Survey.id==stmt2.c.survey_id)




from app import db, models
from app.models import Answer, Question,Section,Survey
from sqlalchemy.orm import aliased

stmt1 = db.session.query(Question).filter(Question.section_id==Section.id,Section.root_id==1).subquery()
stmt2 = db.session.query(Answer).filter(Answer.user_id==1).subquery()

question1= aliased(Question, stmt1)
answer1= aliased(Answer, stmt2)

for q, ans  in db.session.query(question1, answer1).outerjoin(answer1, question1.id == answer1.question_id): print q, ans


