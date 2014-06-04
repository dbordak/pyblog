from webapp2 import WSGIApplication, Route
from google.appengine.api import users
import blargh
import admin
import util
import logging


def handle404(request, response, exception):
    logging.exception(exception)
    template_values = util.genSidebar(users.get_current_user())
    template = util.jinja_template('errors/404')
    response.write(template.render(template_values))


def handle500(request, response, exception):
    logging.exception(exception)
    template = util.jinja_template('errors/500')
    # Don't render anything in case it caused the 500
    response.write(template.render({}))


application = WSGIApplication([
    ('/', blargh.MainPage),
    Route('/<year:\d{4}>/<month:\d{1,2}>/<title>/<entid>',
          handler=blargh.EntryPage),
    Route('/cat/<catid>', handler=blargh.CategoryPage),
    ('/about', blargh.AboutPage)
], debug=True)

admin_app = WSGIApplication([
    ('/admin/', admin.NavPage),
    ('/admin/add/ent', admin.AddEntryPage),
    ('/admin/del/ent', admin.DeleteEntryPage),
    ('/admin/add/cat', admin.AddCategoryPage),
    ('/admin/del/cat', admin.DeleteCategoryPage),
], debug=True)

application.error_handlers[404] = handle404
# application.error_handlers[500] = handle500

admin_app.error_handlers[404] = handle404
# admin.error_handlers[500] = handle500
