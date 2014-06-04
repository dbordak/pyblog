from common import util

render = lambda x, y: util.render(util.jinja_template('admin', x), y)


def render_form(name, form, values):
    values['title'] = name
    values['form'] = form.as_widget()
    return render('form', values)
