from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import Session, relationship, backref,\
                                joinedload_all
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method


Base = declarative_base()

class Section(Base):
    '''A table with sections of a Survey
    '''
    __tablename__ = 'section'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Tittle for this section
    title = Column(String(128), nullable = False)
    #: description for this section
    ## Relationships
    #: Section have zero or more questions 
    questions = relationship('Question', 
        # cascade deletions
        cascade="all, delete-orphan",
        backref = 'section', lazy = 'dynamic')
    #: section belongs to zero or more sections
    parent_id = Column(Integer, ForeignKey('section.id'))
    # children = relationship('Section',
    #     # cascade deletions
    #     cascade="all, delete-orphan",
    #     backref=backref('parent', remote_side=id),
    #     single_parent=True,
    #     lazy = 'dynamic', uselist = True)
    # parent = relationship("section", remote_side=[id])
    # children = relationship("section")
    children = relationship('Section',
        # cascade deletions
        cascade="all, delete-orphan",
        backref=backref('section', remote_side=id),
        lazy = 'dynamic', uselist = True)
    # __mapper_args__ = {
    #     'polymorphic_on' : type
    # }
    @hybrid_property
    def section1(self):
        '''return survey 
        '''
        print "jaja"
        section = self
        while (section.section is not None):
            section = section.section
        return section.id
    @section1.expression
    def section1(cls):
        section = cls.section
        s_ant = section
        print "jeje"
        while (section is not None):
            print "jiji"
            s_ant = section
            section = section.section
        return s_ant.id
    def __repr__(self):
        return "<Section(id='%s', title='%s')>" % (
          self.id, self.title)


class Question(Base):
    '''A table with Questions
    '''
    __tablename__ = 'question'
    #: unique id (automatically generated)
    id = Column(Integer, primary_key = True)
    #: Text for this question
    text = Column(String, nullable = False)
    section_id = Column(Integer, ForeignKey('section.id'))
    def __repr__(self):
        return "<Question(id='%s', text='%s')>" % (
          self.id, self.text)
    @hybrid_property
    def survey(self):
        '''return survey 
        '''
        section = self.section
        while (section.parent is not None):
            section = section.parent
        return section




engine = create_engine('sqlite://', echo=False)
Base.metadata.create_all(engine)
session = Session(engine)


s1=Section(title="1")
session.add(s1)
s2 = Section(title="1.1",section=s1)
session.add(s2)
session.commit()
s3 = Section(title="1.1.1", section = s2)
session.add(s3)
session.commit()
s31 = session.query(Section).get(3)
s11 = session.query(Section).get(1)



q1= Question(text="question1",section=s2)
session.add(q1)
session.commit()

q11 = session.query(Question).get(1)



for s in session.query(Section).filter(Section.section1==1):print s
for s in session.query(Section).filter_by(Section.section1=1):print s



