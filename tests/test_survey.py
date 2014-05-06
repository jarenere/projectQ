from __future__ import division

import unittest
from flask import current_app
from app import app,db
from app.models import User,ROLE_RESEARCHER
from app.models import Survey, Section
import os
from config import basedir

class ModelsTestCase(unittest.TestCase):
    '''test models'''

    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_sequence_sections_exclusive(self):
        '''test function  sequenceSections(sections)'''

        # create a user
        u = User(nickname = 'john', email = 'john@example.com', 
            role = ROLE_RESEARCHER)
        db.session.add(u)
        db.session.commit()
    
        survey = Survey(title = "test",researcher = u)
        s1 = Section (title = "1",description = "a",
            sequence = 1, percent = 1, survey = survey)
        s11 = Section (title = "1.1", description = "a",
            sequence = 1, percent = 0.5, parent = s1)
        s12 = Section (title = "1.1", description = "a",
            sequence = 1, percent = 0.5, parent = s1)
        s111 = Section (title = "1.1", description = "a",
            sequence = 1, percent = 0.5, parent = s11)
        s112 = Section (title = "1.1", description = "a",
            sequence = 1, percent = 0.5, parent = s11)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(s11)
        db.session.add(s12)
        db.session.add(s111)
        db.session.add(s112)
        db.session.commit()
        path1 = 0
        path2 = 0
        path3 = 0
        n = 1000
        error = 0.1
        for i in range(n):
            l = Section.sequenceSections(survey.sections)
            if l ==[s1.id,s11.id,s111.id]:
                path1= path1+1
            elif l ==[s1.id,s11.id,s112.id]:
                path2 = path2 +1
            elif l == [s1.id,s12.id]:
                path3 = path3 +1
            else:
                print l
                assert False == True
                
        assert (path1 in range(int(round(n/4 - error*(n/4))),int(round(n/3 + error*(n/3)))))==True
        assert (path2 in range(int(round(n/4 - error*(n/4))),int(round(n/3 + error*(n/3)))))==True
        assert (path3 in range(int(round(n/2 - error*(n/2))),int(round(n/3 + error*(n/3)))))==True


    def test_sequence_sections_order(self):
        '''test function  sequenceSections(sections)'''

        u = User(nickname = 'john', email = 'john1@example.com', 
            role = ROLE_RESEARCHER)
        db.session.add(u)
        db.session.commit()
        survey = Survey(title = "test",researcher = u)
        s1 = Section (title = "1",description = "a",
            sequence = 1, percent = 1, survey = survey)
        s2 = Section (title = "1",description = "a",
            sequence = 2, percent = 1, survey = survey)
        s3 = Section (title = "1",description = "a",
            sequence = 2, percent = 1, survey = survey)
        s4 = Section (title = "1",description = "a",
            sequence = 2, percent = 1, survey = survey)
        s5 = Section (title = "1",description = "a",
            sequence = 3, percent = 1, survey = survey)
        s6 = Section (title = "1",description = "a",
            sequence = 3, percent = 1, survey = survey)
        db.session.add(survey)
        db.session.add(s1)
        db.session.add(s2)
        db.session.add(s3)
        db.session.add(s4)
        db.session.add(s5)
        db.session.add(s6)
        db.session.commit()
        s1 = s1.id
        s2 = s2.id
        s3 = s3.id
        s4 = s4.id
        s5 = s5.id
        s6 = s6.id
        n = 10000
        error = 0.1
        count = 12
        rango = range(int(round(n/count - error*(n/count))),int(round(n/3 + error*(n/3))))
        dic ={}
        for i in range(n):
            l = tuple(Section.sequenceSections(survey.sections))
            if dic.has_key(l):
                dic[l] = dic[l]+1
            else:
                dic[l] = 0
        print dic
        assert dic.has_key((s1,s2,s3,s4,s5,s6)) == True and dic[s1,s2,s3,s4,s5,s6] in rango
        assert dic.has_key((s1,s2,s3,s4,s6,s5)) == True and dic[s1,s2,s3,s4,s6,s5] in rango
        assert dic.has_key((s1,s2,s4,s3,s5,s6)) == True and dic[s1,s2,s4,s3,s5,s6] in rango
        assert dic.has_key((s1,s2,s4,s3,s6,s5)) == True and dic[s1,s2,s4,s3,s6,s5] in rango
        assert dic.has_key((s1,s3,s2,s4,s5,s6)) == True and dic[s1,s3,s2,s4,s5,s6] in rango
        assert dic.has_key((s1,s3,s2,s4,s6,s5)) == True and dic[s1,s3,s2,s4,s6,s5] in rango
        assert dic.has_key((s1,s3,s4,s2,s5,s6)) == True and dic[s1,s3,s4,s2,s5,s6] in rango
        assert dic.has_key((s1,s3,s4,s2,s6,s5)) == True and dic[s1,s3,s4,s2,s6,s5] in rango
        assert dic.has_key((s1,s4,s2,s3,s5,s6)) == True and dic[s1,s4,s2,s3,s5,s6] in rango
        assert dic.has_key((s1,s4,s2,s3,s6,s5)) == True and dic[s1,s4,s2,s3,s6,s5] in rango
        assert dic.has_key((s1,s4,s3,s2,s5,s6)) == True and dic[s1,s4,s3,s2,s5,s6] in rango
        assert dic.has_key((s1,s4,s3,s2,s6,s5)) == True and dic[s1,s4,s3,s2,s6,s5] in rango
        assert len(dic)== count












if __name__ == '__main__':
    unittest.main()