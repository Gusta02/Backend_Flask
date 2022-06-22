from flask import abort, render_template, request, render_template_string
from flask import Blueprint
import os
from flask import abort

from config import TEMPLATE_FOLDER,get_connection


error = Blueprint("error",__name__, 
        template_folder=os.path.join(TEMPLATE_FOLDER, "resources", "templates"), 
        static_folder=os.path.join(TEMPLATE_FOLDER, "resources", "static"))

@error.errorhandler(404)
def page_not_found(e):
    #retorna erro 500
    print(e)
    return render_template('error_404.html'), 404


@error.errorhandler(500)
def internal_server_error(e):
    # retorna erro 500
    print(e)
    return render_template('error_404.html'), 500


@error.errorhandler(500)
def handle_500(e):
    original = getattr(e, "original_exception", None)

    if original is None:
        # direct 500 error, such as abort(500)
        return render_template("500.html"), 500

    # wrapped unhandled error
    return render_template("500_unhandled.html", e=original), 500


@error.errorhandler(TypeError)
def special_exception_handler(e):
    print(e)
    return 'Database connection failed', 500