"""
Shared Flask extension instances.

Defined here to avoid circular imports between app.py and blueprint modules.
Import these into app.py for init_app(), and into blueprints for decorators.
"""
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

csrf = CSRFProtect()
limiter = Limiter(key_func=get_remote_address, default_limits=[])
