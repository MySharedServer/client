# -*- coding: utf-8 -*-

import os


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s %(filename)s[line:%(lineno)d] [%(levelname)s] %(message)s'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',  # Size Rotation
            'filename': os.path.join(BASE_DIR, 'django.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'requestReply': {
            'class': 'logging.handlers.RotatingFileHandler',  # Size Rotation
            'filename': os.path.join(BASE_DIR, 'request.log'),
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'class': 'logging.StreamHandler',  # Console
            'filters': ['require_debug_true'],
            'formatter': 'standard',
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['logfile', 'console'],
            'propagate': True,
        },
        'request': {
            'level': 'INFO',
            'handlers': ['requestReply'],
            'propagate': True,
        }
    }
}
