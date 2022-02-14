from horseman.http import HTTPError
from reiter.form import FormView
from reiter.ui import TemplateLoader


TEMPLATES = TemplateLoader("./templates")


class FormPage(FormView):

    template = TEMPLATES['form.pt']

    @property
    def action(self):
        return (
            self.request.application_uri() + self.request.route.path
        )

    def setupForm(self, data=None, formdata=None):
        raise NotImplementedError('implement your own.')

    def GET(self):
        form = self.setupForm()
        return dict(form=form, error=None)

    def POST(self):
        data = self.request.extract()
        action = data.form.get('form.trigger')  # can be None.
        if action:
            return self.process_action(action)
        return HTTPError(400)
