from functools import partial
from dataclasses import dataclass, field
from reiter.application.app import Application
from reiter.application.request import Request
from reiter.ui import TemplateLoader
from reiter.ui.components import Page
from reiter.ui.registry import UIRegistry
from reiter.view.utils import routables
from roughrider.routing.components import NamedRoutes


TEMPLATES = TemplateLoader("./templates")


class Request(Request):

    @property
    def user(self):
        return None


@dataclass
class Reiter(Application):

    ui: UIRegistry = field(default_factory=UIRegistry)
    routes: NamedRoutes = field(
        default_factory=partial(NamedRoutes, extractor=routables))

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].encode('latin-1').decode('utf-8') or '/'
        response = self.resolve(path, environ)
        return response(environ, start_response)

    def get_actions(self, *args, **kwargs):
        return []

app = Reiter()


import reha.siguv_theme
reha.siguv_theme.install_theme(app, request_type=Request)

#@app.ui.register_layout(Request)
#class Layout:
#
#    _template = TEMPLATES["layout.pt"]
#
#    def __init__(self, request, name):
#        self.name = name
#
#    def render(self, content, **namespace):
#        return self._template.render(content=content, **namespace)


@app.routes.register('/')
class Index(Page):
    template = TEMPLATES['index']

    def GET(self):
        return {}


@app.routes.register('/favicon.ico')
class Index(Page):

    def GET(self):
        return "" 
