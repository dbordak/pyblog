"""Functions and settings commonly used by blargh.py and admin.py"""

from google.appengine.api import users
from blargh import models


def genSidebar(user=None):
    """Generate a standard template_values for the sidebar"""
    return {
        'isAdmin': user and users.is_current_user_admin(),
        'cats': models.Category.query()
    }
