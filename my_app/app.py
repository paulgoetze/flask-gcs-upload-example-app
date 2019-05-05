from os import path
from typing import Dict, Optional

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from my_app.error_handling import register_error_handlers

APP_ROOT = path.dirname(path.abspath(__file__))

db = SQLAlchemy()
migrate = Migrate()


class App(Flask):

    def __init__(self, config: Optional[Dict] = None):
        Flask.__init__(self, __name__)

        self.url_map.strict_slashes = False
        self.load_config()

        if config:
            self.config.update(config)

        register_error_handlers(self)
        self.register_blueprints()
        self.setup_depots()

        db.init_app(self)
        migrate.init_app(self, db)

    def load_config(self):
        """Load the app's config from app_config.py"""

        file_path = path.join(APP_ROOT, 'config', 'app_config.py')
        self.config.from_pyfile(file_path)

    def register_blueprints(self):
        """Register all blueprints"""

        from .users import users
        self.register_blueprint(users)

    def setup_depots(self):
        """Setup the file depots"""

        from .config import depot
        depot.init_depots(self)
        depot.make_middleware(self)
