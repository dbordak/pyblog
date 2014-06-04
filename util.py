"""Functions and settings commonly used by blargh.py and admin.py"""

from os.path import dirname
from google.appengine.api import users
import jinja2
import logging
from models import Category

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(__file__)))

jinja_template = lambda x: JINJA_ENVIRONMENT.get_template(
    'templates/' + x + '.html'
)


def genSidebar(user=None):
    """Generate a standard template_values for the sidebar"""
    return {
        'isAdmin': user and users.is_current_user_admin(),
        'cats': Category.query()
    }


def handle404(request, response, exception):
    logging.exception(exception)
    template_values = genSidebar(users.get_current_user())
    template = jinja_template('errors/404')
    response.write(template.render(template_values))


def handle500(request, response, exception):
    logging.exception(exception)
    template = jinja_template('errors/500')
    # Don't render anything in case it caused the 500
    response.write(template.render({}))
