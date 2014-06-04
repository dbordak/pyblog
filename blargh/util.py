from google.appengine.datastore.datastore_query import Cursor
from common import util #jinja_template, genSidebar, render
import models

render = lambda x, y: util.render(util.jinja_template('blargh', x), y)


def getPage(query, req, qty=10):
    """Gets items for constructing a page, and the next cursor object for
    getting the next page."""
    qolder = query.order(-models.Entry.date)
    qnewer = query.order(models.Entry.date)
    curs = Cursor(urlsafe=req.args.get('cursor'))

    entries, next_curs, more = qolder.fetch_page(qty, start_cursor=curs)
    _, prev_curs, less = qnewer.fetch_page(qty, start_cursor=curs.reversed())

    buttons = (
        prev_curs.urlsafe() if less and prev_curs else None,
        next_curs.urlsafe() if more and next_curs else None
    )
    return (entries, buttons)


# TODO: This function.
def badGetPage(query, req, qty=10):
    """Like getPage except bad."""
    qolder = query.order(-models.Entry.date)
    entries = qolder.fetch(10)

    return (entries, None)
