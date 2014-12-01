from app.models import *
import utiles
from app.game.game import Games


def premios():
    utiles.borrarJuegos()
    utiles.borrarImpaciencia()
    utiles.borrarRaffle()
    
    game = Games(1)
    users = StateSurvey.query.filter(StateSurvey.survey_id==1,\
        StateSurvey.status.op('&')(StateSurvey.FINISH_OK))
    for u in users:
        game.part2_reimplement(u.user)
        # print u.user.id, u.user.email
    game.match()
    for u in users:
        game.raffle(u.user)

    raffle = Raffle.query.filter(Raffle.prize!=0)
    gameA = Game.query.filter(Game.prizeA)
    gameB = Game.query.filter(Game.prizeB)
    impatience = GameImpatience.query.filter(GameImpatience.prize)
    sum_raffle = sum(r.prize for r in raffle)
    sum_decisions = sum (g.moneyA for g in gameA) + \
        sum (g.moneyB for g in gameB)
    sum_impatience =  sum (int(i.answer.answerText[8:10]) for i in impatience)
    sum_total =  sum_raffle + sum_decisions + sum_impatience
    f = open ("prueba.txt","a")
    f.write("Total: %s \n" % (sum_total))
    f.write("rifa: %s \n" % (sum_raffle))
    f.write("decisiones: %s \n" % (sum_decisions))
    f.write("impaciencia: %s \n" % (sum_impatience))
    f.write("\n\n")
    f.close()
    return sum_total

def go():
    min=False
    max = False
    i=0
    while (min==False or max==False):
        sum_total=premios()
        if sum_total<600:
            min=True
            f = open ("prueba.txt","a")
            f.write("minimo conseguido en: %s \n" % (i))
            f.close()
            print ("minimo conseguido en: %s \n" % (i))
        if sum_total>1400:
            max=True
            f = open ("prueba.txt","a")
            f.write("maximo conseguido en: %s \n" % (i))
            f.close()
            print ("maximo conseguido en: %s \n" % (i))
        i = i+1
