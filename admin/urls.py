# -*- coding: utf-8 -*-
# admin.urls
#

from kay.routing import ViewGroup, Rule

view_groups = [ViewGroup(
    Rule('/', endpoint='index', view='admin.views.NavPage'),
    Rule('/add/ent', endpoint='adde', view='admin.views.AddEntryPage'),
    Rule('/del/ent', endpoint='dele', view='admin.views.DeleteEntryPage'),
    Rule('/add/cat', endpoint='addc', view='admin.views.AddCategoryPage'),
    Rule('/del/cat', endpoint='delc', view='admin.views.DeleteCategoryPage'),
)]
