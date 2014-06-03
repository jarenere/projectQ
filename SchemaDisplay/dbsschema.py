import sadisplay
from app import models
import os

desc = sadisplay.describe([models.Survey, models.Consent,models.Section,models.Question, models.Condition, models.User, models.StateSurvey,models.Answer])
open('schema1_alto_nivel.dot', 'w').write(sadisplay.dot(desc))
os.system("dot -Tsvg schema1_alto_nivel.dot > schema1_alto_nivel.svg")

#esquema preguntas:
desc = sadisplay.describe([models.Question,models.QuestionText,models.QuestionYN, models.QuestionChoice, models.QuestionLikertScale])
open('preguntas.dot', 'w').write(sadisplay.dot(desc))
os.system("dot -Tsvg preguntas.dot > preguntas.svg")

#esquema juegos:


desc = sadisplay.describe([models.GameImpatience, models.Game, models.Raffle, models.User, models.Survey])
open('games_sin_detalle.dot', 'w').write(sadisplay.dot(desc))
os.system("dot -Tsvg games_sin_detalle.dot > games_sin_detalle.svg")

desc = sadisplay.describe([models.Game, models.GameLottery1, models.GameLottery2, models.GameRent1, models.GameRent2, models.GameUltimatum, models.GameDictador])
open('games.dot', 'w').write(sadisplay.dot(desc))
os.system("dot -Tsvg games.dot > games.svg")

#esquema base de datos
os.system("sadisplay -u sqlite:////home/jarenere/frame_game_theory_esquemas/data-dev.sqlite -i answer,condition,consent,question,section,stateSurvey,survey,user -r dot > schema_bbdd.dot")
os.system("dot -Tsvg schema_bbdd.dot > schema_bbdd.svg")

os.system("sadisplay -u sqlite:////home/jarenere/frame_game_theory_esquemas/data-dev.sqlite -i answer,user,raffle,gameRentSeeking,survey -r dot > schema_bbdd_game.dot")
os.system("dot -Tsvg schema_bbdd_game.dot > schema_bbdd_game.svg")
