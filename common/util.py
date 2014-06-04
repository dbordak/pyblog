"""Functions and settings commonly used by blargh.py and admin.py"""

from os.path import dirname
from google.appengine.api import users
from kay.utils import render_to_response
import jinja2
from blargh import models

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(dirname(dirname(__file__))))

jinja_template = lambda x, y: JINJA_ENVIRONMENT.get_template(
    x + '/templates/' + y + '.html'
)

render = render_to_response


def genSidebar(user=None):
    """Generate a standard template_values for the sidebar"""
    return {
        'isAdmin': user and users.is_current_user_admin(),
        'cats': models.Category.query()
    }
