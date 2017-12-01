from flask_cache import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_assets import Environment

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

debug_toolbar = DebugToolbarExtension()