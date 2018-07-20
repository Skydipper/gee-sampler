"""The API MODULE"""

import os
import json
import logging
import ee
from flask import Flask
from gee_sampler.config import SETTINGS
from gee_sampler.routes.api import error
from gee_sampler.routes.api.v1 import sampler_endpoints
from gee_sampler.utils.files import load_config_json
import CTRegisterMicroserviceFlask
from oauth2client.service_account import ServiceAccountCredentials

logging.basicConfig(
    level=SETTINGS.get('logging', {}).get('level'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y%m%d-%H:%M%p',
)

# GEE init
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

# CT
info = load_config_json('register')
swagger = load_config_json('swagger')

logging.debug("Registering microservice")
CTRegisterMicroserviceFlask.register(
    app=app,
    name='gee_sampler',
    info=info,
    swagger=swagger,
    mode = CTRegisterMicroserviceFlask.AUTOREGISTER_MODE if os.getenv('CT_REGISTER_MODE') and os.getenv('CT_REGISTER_MODE') == 'auto' else CTRegisterMicroserviceFlask.NORMAL_MODE,
    ct_url=os.getenv('CT_URL'),
    url=os.getenv('LOCAL_URL'),
    api_version='v1'
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
