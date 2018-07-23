"""-"""
from gee_sampler.utils.files import BASE_DIR
import os


SETTINGS = {
    'logging': {
        'level': 'DEBUG'
    },
    'service': {
        'port': os.getenv('PORT')
    },
    'gee': {
        'service_account': '',
        'privatekey_file': BASE_DIR + '/privatekey.pem'
    }
}
