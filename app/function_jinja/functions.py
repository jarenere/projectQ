def status_part2(status):
    from app.models import StateSurvey
    if status & StateSurvey.PART2_MONEY:
        return u'Money Real'
    else:
        return u'Untrue money'


def status_part3(status):
    from app.models import StateSurvey
    if status & StateSurvey.PART3_MONEY:
        return u'Money Real'
    else:
        return u'Untrue money'