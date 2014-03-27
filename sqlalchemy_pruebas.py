from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, relationship, backref,\
                                joinedload_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection


Base = declarative_base()


class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  name = Column(String)
  fullname = Column(String)
  password = Column(String)
  def __repr__(self):
    return "<User(name='%s', fullname='%s', password='%s')>" % (
      self.name, self.fullname, self.password)


class Address(Base):
  __tablename__ = 'addresses'
  id = Column(Integer, primary_key=True)
  email_address = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id'))
  user = relationship("User", backref=backref('addresses', order_by=id))
  def __repr__(self):
    return "<Address(email_address='%s')>" % self.email_address


engine = create_engine('sqlite://', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


user1=User(name="name1",fullname="fullname1",password="password1")
session.add(user1)
user2=User(name="name2",fullname="fullname2",password="password2")
session.add(user2)
user3=User(name="name3",fullname="fullname3",password="password3")
session.add(user3)
session.commit()

email1=Address(email_address="user1@", user=user1)
session.add(email1)
session.commit()
email12=Address(email_address="user1_2@", user=user1)
session.add(email12)
session.commit()
email2=Address(email_address="user2@", user=user2)
session.add(email2)
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


