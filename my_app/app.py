from os import path

from flask import Flask

APP_ROOT = path.dirname(path.abspath(__file__))


class App(Flask):

    def __init__(self):
        Flask.__init__(self, __name__)

        self.load_config()
        self.setup_depots()

    def load_config(self):
        """Load the app's config from app_config.py"""

        file_path = path.join(APP_ROOT, 'config', 'app_config.py')
        self.config.from_pyfile(file_path)

    def setup_depots(self):
        """Setup the file depots"""

        from .config import depot
        depot.init_depots(self)


app = App()
