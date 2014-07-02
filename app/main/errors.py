from flask import render_template
from . import blueprint

@blueprint.app_errorhandler(403)
def forbidden(error):
    return render_template('403.html',title = 'Forbidden'), 403

@blueprint.app_errorhandler(404)
def internal_error(error):
    return render_template('404.html', title='File Not Found'), 404

@blueprint.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html', title='Internal Server Error'), 500


class ErrorExceeded(Exception):
    pass

class ErrorTimedOut(Exception):
    pass

class ErrorEndDateOut(Exception):
    pass



@blueprint.app_errorhandler(ErrorExceeded)
def error_excedeed(error):
    return render_template('/surveys/error_exceeded.html',
        title = 'maximum number of surveys exceeded ')


@blueprint.app_errorhandler(ErrorTimedOut)
def error_timed_out(error):
    return render_template('/surveys/error_time_date.html',
        title = 'Time out')


@blueprint.app_errorhandler(ErrorEndDateOut)
def error_end_date_out(error):
    return render_template('/surveys/error_time_date.html',
        title = 'End date out')