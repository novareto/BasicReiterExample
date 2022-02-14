import pathlib
import fanstatic
import http_session
import http_session_file
import reiter.auth.components
import reiter.auth.filters

from functools import partial
from roughrider.sqlalchemy.component import SQLAlchemyEngine
from app import app


#### Registering middlewares.
session_environ = "session"

session = http_session.SignedCookieManager(
    http_session_file.FileStore(
        pathlib.Path('./sessions'), 3000
    ),
    'secret', salt='salt', cookie_name='cookie', TTL=3000
)

session_getter = reiter.auth.components.session_from_environ(
    session_environ
)

# Auth
authentication = reiter.auth.components.Auth(
    sources=[],
    user_key="principal",
    session_getter=session_getter,
    filters=(
        reiter.auth.filters.security_bypass([
            "/login"
        ]),
        reiter.auth.filters.secured(path="/login"),
    )
)

sqlsession = SQLAlchemyEngine.from_url(
    name='sql', url='sqlite:///example.db'
)

app.middlewares.add(partial(
    fanstatic.Fanstatic,
    compile=False,
    recompute_hashes=True,
    bottom=True,
    publisher_signature="static"
), 10)

app.middlewares.add(partial(
    session.middleware,
    environ_key=session_environ,
    secure=False
), 20)

app.middlewares.add(sqlsession('sql'), 30)
app.middlewares.add(authentication, 40)

#### Registering utilities
app.utilities['authentication'] = authentication
app.utilities['sql'] = sqlsession
