"""The API MODULE"""

import os
import json
import logging
import colorama
from flask import Flask
from gee_sampler.config import SETTINGS
from gee_sampler.routes.api import error
from gee_sampler.routes.api.v1 import sampler_endpoints
#, pstwo_endpoints
from gee_sampler.utils.files import load_config_json
import CTRegisterMicroserviceFlask
import ee
from oauth2client.service_account import ServiceAccountCredentials

LOG_COLORS = {
            'INFO': colorama.Fore.GREEN,
            'ERROR': colorama.Fore.RED,
            'WARNING': colorama.Fore.YELLOW
        }
class ColorFormatter(logging.Formatter):
    def format(self, record, *args, **kwargs):
        # if the corresponding logger has children, they may receive modified
        # record, so we want to keep it intact
        new_record = copy.copy(record)
        if new_record.levelno in LOG_COLORS:
            # we want levelname to be in different color, so let's modify it
            new_record.levelname = "{color_begin}{level}{color_end}".format(
                level=new_record.levelname,
                color_begin=LOG_COLORS[new_record.levelno],
                color_end=colorama.Style.RESET_ALL,
            )
        # now we can let standart formatting take care of the rest
        return super(ColorFormatter, self).format(new_record, *args, **kwargs)

logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format= "%(asctime)s - %(name)s - %(levelname)s - line: %(lineno)s: %(message)s",
    datefmt='%Y%m%d-%H:%M%p'
)
formatter = ColorFormatter("%(asctime)s - %(name)s - %(levelname)s - line: %(lineno)s: %(message)s")

# this handler will write to sys.stderr by default
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger(__name__).addHandler(handler)


# # Initializing GEE
gee = SETTINGS.get('gee')
gee_credentials = ServiceAccountCredentials.from_p12_keyfile(
    gee.get('service_account'),
    gee.get('privatekey_file'),
    scopes=ee.oauth.SCOPE
)

ee.Initialize(gee_credentials)
ee.data.setDeadline(60000)

# Flask App
app = Flask(__name__)

# Routing
app.register_blueprint(sampler_endpoints, url_prefix='/api/v1/sampler')
#app.register_blueprint(pstwo_endpoints, url_prefix='/api/v1/pstwo')

# CT
info = load_config_json('register')
swagger = load_config_json('swagger')
CTRegisterMicroserviceFlask.register(
    app=app,
    name='gee_sampler',
    info=info,
    swagger=swagger,
    mode=CTRegisterMicroserviceFlask.AUTOREGISTER_MODE if os.getenv('CT_REGISTER_MODE') and os.getenv('CT_REGISTER_MODE') == 'auto' else CTRegisterMicroserviceFlask.NORMAL_MODE,
    ct_url=os.getenv('CT_URL'),
    url=os.getenv('LOCAL_URL')
)


@app.errorhandler(403)
def forbidden(e):
    return error(status=403, detail='Forbidden')


@app.errorhandler(404)
def page_not_found(e):
    return error(status=404, detail='Not Found')


@app.errorhandler(405)
def method_not_allowed(e):
    return error(status=405, detail='Method Not Allowed')


@app.errorhandler(410)
def gone(e):
    return error(status=410, detail='Gone')


@app.errorhandler(500)
def internal_server_error(e):
    return error(status=500, detail='Internal Server Error')
