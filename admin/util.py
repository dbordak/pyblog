from kay.utils import render_to_response


def render_form(name, form, values):
    values['title'] = name
    values['form'] = form.as_widget()
    return render_to_response('admin/form.html', values)
