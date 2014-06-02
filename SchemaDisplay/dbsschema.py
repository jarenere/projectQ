from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
# sqlite:////home/jarenere/frame_game_theory/data-test.sqlite
# create the pydot graph object by autoloading all tables via a bound metadata object
# graph = create_schema_graph(metadata=MetaData('postgres://user:pwd@host/database'),
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/jarenere/frame_game_theory/data-dev.sqlite'
graph = create_schema_graph(metadata=MetaData(SQLALCHEMY_DATABASE_URI),
   show_datatypes=False, # The image would get nasty big if we'd show the datatypes
   show_indexes=False, # ditto for indexes
   rankdir='LR', # From left to right (instead of top to bottom)
   concentrate=False # Don't try to join the relation lines together
)
graph.write_png('dbschema.png') # write out the file



from myapp import model
from sqlalchemy_schemadisplay import create_uml_graph
from sqlalchemy.orm import class_mapper

# lets find all the mappers in our model
mappers = []
for attr in dir(model):
    if attr[0] == '_': continue
    try:
        cls = getattr(model, attr)
        mappers.append(class_mapper(cls))
    except:
        pass

# pass them to the function and set some formatting options
graph = create_uml_graph(mappers,
    show_operations=False, # not necessary in this case
    show_multiplicity_one=False # some people like to see the ones, some don't
)
graph.write_png('schema.png') # write out the file


---------

import sadisplay
from app import models
desc = sadisplay.describe([getattr(models, attr) for attr in dir(models)])
open('schema.plantuml', 'w').write(sadisplay.plantuml(desc))
open('schema.dot', 'w').write(sadisplay.dot(desc))

# Or only part of schema
desc = sadisplay.describe([model.User, model.Group, model.Permission])
open('auth.plantuml', 'w').write(sadisplay.plantuml(desc))
open('auth.dot', 'w').write(sadisplay.dot(desc))


# esquema principal:



desc = sadisplay.describe([models.Survey, models.Consent,models.Section,models.Question, models.Condition, models.User, models.StateSurvey,models.Answer])
open('schema1.plantuml', 'w').write(sadisplay.plantuml(desc))
ataopen('schema1.dot', 'w').write(sadisplay.dot(desc))

$ java -jar plantuml.jar -Tsvg schema1.plantuml
$ dot -Tpng schema1.dot > schema1.png

desc = sadisplay.describe([models.Survey, models.Consent,models.Section,models.Question, models.Condition, models.User, models.StateSurvey, models.Answer],show_methods=False,show_properties=False)
open('schema2.plantuml', 'w').write(sadisplay.plantuml(desc))
open('schema2.dot', 'w').write(sadisplay.dot(desc))

$ java -jar plantuml.jar -Tsvg schema2.plantuml
$ dot -Tpng schema2.dot > schema2.png


#esquema preguntas:
desc = sadisplay.describe([models.Question,models.QuestionText,models.QuestionYN, models.QuestionChoice, models.QuestionLikertScale])
open('question.dot', 'w').write(sadisplay.dot(desc))

dot -Tsvg question.dot > question.svg


#esquema de juegos
desc = sadisplay.describe([models.GameImpatience, models.Game, models.GameLottery1, models.GameLottery2, models.GameRent1, models.GameRent2, models.GameUltimatum, models.GameDictador, models.Raffle, models.User, models.Survey])
open('games.dot', 'w').write(sadisplay.dot(desc))
$ dot -Tsvg games.dot > games.svg


---
$ sadisplay -u sqlite:////home/jarenere/frame_game_theory/data-dev.sqlite -r dot > schema.dot
$ dot -Tpng db_schema.dot > db_schema.png

---