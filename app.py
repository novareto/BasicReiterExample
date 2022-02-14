from functools import partial
from dataclasses import dataclass, field
from reiter.ui import TemplateLoader
from reiter.ui.registry import UIRegistry
from reiter.ui.components import Page
from reiter.view.utils import routables
from roughrider.routing.components import NamedRoutes
from roughrider.application import WrappableApplication
import login


TEMPLATES = TemplateLoader("./templates")


@dataclass
class Reiter(WrappableApplication):
    ui: UIRegistry = field(default_factory=UIRegistry)
    routes: NamedRoutes = field(
        default_factory=partial(NamedRoutes, extractor=routables))


app = Reiter()


@app.routes.register('/')
class Index(Page):
    template = TEMPLATES['index']

    def GET(self):
        return {}


@app.routes.register('/favicon.ico')
class Index(Page):

    def GET(self):
        return ""


app.routes.register('/login')(login.LoginForm)
