from copy import copy

from depot.manager import DepotManager
from flask import Flask

AVATAR_DEPOT = 'avatar'
BACKGROUND_DEPOT = 'background'

DEPOTS = {
    AVATAR_DEPOT: {'depot.prefix': 'avatars/'},
    BACKGROUND_DEPOT: {'depot.prefix': 'backgrounds/'}
}


def init_depots(app: Flask):
    """Setup all configured depots"""

    config = default_config(app)

    for (name, special_config) in DEPOTS.items():
        depot_config = copy(config)
        depot_config.update(special_config)
        DepotManager.configure(name, depot_config)


def default_config(app: Flask):
    """Return a default config that is used by all depots"""

    if app.testing:
        return test_config()
    else:
        return production_config(app)


def test_config():
    """Return the default test config that is used by all depots"""

    return {'depot.backend': 'depot.io.memory.MemoryFileStorage'}


def production_config(app: Flask):
    """Return the default production config that is used by all depots"""

    return {
        'depot.backend': 'depot.io.boto3.S3Storage',
        'depot.endpoint_url': 'https://storage.googleapis.com',
        'depot.access_key_id': app.config.get('GOOGLE_CLOUD_STORAGE_ACCESS_KEY'),
        'depot.secret_access_key': app.config.get('GOOGLE_CLOUD_STORAGE_SECRET_KEY'),
        'depot.bucket': app.config.get('GOOGLE_CLOUD_STORAGE_BUCKET')
    }


def make_middleware(app):
    """Make the depot middle to serve uploads through the /depot endpoint"""

    app.wsgi_app = DepotManager.make_middleware(app.wsgi_app)
