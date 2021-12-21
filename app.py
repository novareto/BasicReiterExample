import typing as t
import fanstatic
from functools import partial
from dataclasses import dataclass, field
from reiter.application.app import Application
from reiter.application.request import Request as BaseRequest
from reiter.ui import TemplateLoader
from reiter.ui.components import Page
from reiter.ui.registry import UIRegistry
from reiter.view.utils import routables
from reha.siguv_theme import get_theme
from roughrider.routing.components import NamedRoutes


TEMPLATES = TemplateLoader("./templates")


class Request(BaseRequest):
    user = None


@dataclass
class Reiter(Application):

    request_factory: Request = field(default=Request)
    ui: UIRegistry = field(
        default_factory=partial(get_theme, request_type=Request))
    routes: NamedRoutes = field(
        default_factory=partial(NamedRoutes, extractor=routables))

    def get_actions(self, *args, **kwargs):
        return []

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO'].encode('latin-1').decode('utf-8')
        response = self.resolve(path, environ)
        return response(environ, start_response)


reiter = Reiter()


@reiter.routes.register('/')
class Index(Page):
    template = TEMPLATES['index']

    def GET(self):
        return {}



app = fanstatic.Fanstatic(reiter)
