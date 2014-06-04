from kay.utils import forms
from blargh import models


# TODO: Move to util
def populateCategories(include_default=True, include_subcats=True):
    categories = [("None", "---")] if include_default else []
    for cat in models.Category.query():
        if include_subcats or not cat.parent:
            categories.append((cat.key.integer_id(), cat.name))
    return categories


class NewEntryForm(forms.Form):
    def __init__(self):
        super(NewEntryForm, self).__init__()
        self.category.choices = populateCategories()
    title = forms.TextField(required=True)
    category = forms.ChoiceField(choices=[], required=False)
    content = forms.TextField(required=True, widget=forms.Textarea)


class NewCategoryForm(forms.Form):
    def __init__(self):
        super(NewCategoryForm, self).__init__()
        self.parent.choices = populateCategories(include_subcats=False)
    name = forms.TextField(required=True)
    parent = forms.ChoiceField(choices=[], required=False)


class DeleteEntryForm(forms.Form):
    def __init__(self):
        super(DeleteEntryForm, self).__init__()
        self.entry.choices = [
            (ent.key.integer_id(), ent.name)
            for ent in models.Entry.query()
        ]
    entry = forms.ChoiceField(choices=[])


class DeleteCategoryForm(forms.Form):
    def __init__(self):
        super(DeleteCategoryForm, self).__init__()
        self.category.choices = populateCategories(include_default=False)
    category = forms.ChoiceField(choices=[])
