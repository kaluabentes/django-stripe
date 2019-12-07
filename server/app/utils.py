import os
import json

from django.conf import settings

app_config = None

def get_app_config(key):
    base_dir = os.path.dirname(settings.BASE_DIR)
    config_path = os.path.join(base_dir, settings.CONFIG_FILE_NAME)

    with open(config_path) as config:
        try:
            config = json.loads(config.read())
            return config[key]
        except KeyError:
            print('[Error] Config key not exist')


def parse_body(request):
    body_unicode = request.body.decode('utf-8')
    return json.loads(body_unicode)
