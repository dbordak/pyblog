"""All administration pages."""

from google.appengine.ext import ndb
from werkzeug import redirect
from kay.utils import url_for, render_to_response as render

from blargh import models
import forms
from common.util import genSidebar
import util


def AddCategoryPage(request):
    """Administration panel for adding categories"""
    template_values = genSidebar()
    form = forms.NewCategoryForm()

    if request.method == "POST" and form.validate(request.form):
        newCategory = models.Category(name=form['name'])

        if form['parent'] != "None":
            newCategory.parent = ndb.Key(models.Category, int(form['parent']))
        newCategory.put()
        return redirect(url_for('admin/index'))
    return util.render_form('Add Category', form, template_values)


# TODO: CSRF, Wap
def DeleteCategoryPage(request):
    """Administration panel for deleting categories"""
    template_values = genSidebar()
    form = forms.DeleteCategoryForm()

    if request.method == "POST" and form.validate(request.form):
        ndb.Key(models.Category, int(form['category'])).delete()
        return redirect(url_for('admin/index'))

    return util.render_form('Delete Category', form, template_values)


def AddEntryPage(request):
    """Administration panel for adding entries"""
    template_values = genSidebar()
    form = forms.NewEntryForm()

    if request.method == "POST" and form.validate(request.form):
        newEntry = models.Entry(
            title=form['title'],
            content=form['content']
        )

        if form['category'] != "None":
            newEntry.category = ndb.Key(models.Category, int(form['category']))
        newEntry.put()
        return redirect(url_for('admin/index'))

    template_values['form'] = form.as_widget()
    return render('admin/add_ent.html', template_values)


def DeleteEntryPage(request):
    """Administration panel for deleting entries"""
    template_values = genSidebar()
    form = forms.DeleteEntryForm()

    if request.method == "POST":
        ndb.Key(models.Entry, int(form['entry'])).delete()
        return redirect(url_for('admin/index'))

    return util.render_form('Delete Entry', form, template_values)


def NavPage(request):
    """Navigation page for administrative tasks."""
    template_values = genSidebar()
    return render('admin/index.html', template_values)
