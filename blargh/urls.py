# -*- coding: utf-8 -*-
# blargh.urls
#

from kay.routing import (
    ViewGroup, Rule
)

view_groups = [ViewGroup(
    Rule('/', endpoint='index', view='blargh.views.MainPage'),
    Rule('/cat/<catid>', endpoint='cats', view='blargh.views.CategoryPage'),
    Rule('/<int:year>/<int:month>/<title>/<entid>', endpoint='ent',
         view='blargh.views.EntryPage'),
    Rule('/about', endpoint='about', view='blargh.views.AboutPage')
)]
