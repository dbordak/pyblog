"""What will eventually be a blog."""

from google.appengine.api import users
from werkzeug import redirect
import models
import util
from common.util import genSidebar


def MainPage(request):
    """List of blog entry summaries."""
    template_values = genSidebar(users.get_current_user())

    template_values['entries'], template_values['buttons'] = util.getPage(
        models.Entry.query(), request)

    return util.render('index', template_values)


def CategoryPage(request, catid):
    """List of blog entry summaries for a given category, plus any
    child categories."""
    template_values = genSidebar(users.get_current_user())
    cat = models.Category.get_by_id(int(catid))

    if cat.parent is None:
        subcats = models.Category.query(
            models.Category.parent == cat.key
        ).fetch(keys_only=True)
        subcats.append(cat.key)

        entry_query = models.Entry.query(
            models.Entry.category.IN(subcats)
        ).order(-models.Entry.date)

        template_values['entries'], template_values['buttons'] = util.badGetPage(
            entry_query, request)
    else:
        entry_query = models.Entry.query(
            models.Entry.category == cat.key
        ).order(-models.Entry.date)

        template_values['entries'], template_values['buttons'] = util.getPage(
            entry_query, request)

    return util.render('index', template_values)


def EntryPage(request, year, month, title, entid):
    """Individual blog post page"""
    template_values = genSidebar(users.get_current_user())
    ent = models.Entry.get_by_id(int(entid))

    # TODO: Make this look nicer
    if (
        ent.date.month == int(month) and ent.date.year == int(year)
        and ent.title_safe == title
    ):
        template_values['title'] = ent.title
        template_values['content'] = ent.content

        return util.render('entry', template_values)
    else:
        return redirect(ent.url)


def AboutPage(request):
    """About me page"""
    template_values = genSidebar(users.get_current_user())
    return util.render('about', template_values)
