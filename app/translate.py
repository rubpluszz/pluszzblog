import json
import requests
from flask import current_app
from flask_babel import _


def translate(text, dest_language):
    """Функція для перекладу повідомлень заснованана бібліотеці translator"""
    r = ts.google(text, to_language=dest_language, if_use_cn_host=True)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))
