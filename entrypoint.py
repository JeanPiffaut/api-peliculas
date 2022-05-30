import os

from app import create_app

setting_module = os.getenv('APP_SETTINGS_MODULE')
app = create_app(setting_module)