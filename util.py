"""Functions and settings commonly used by blargh.py and admin.py"""

from os.path import dirname
from google.appengine.api import users
import jinja2
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
