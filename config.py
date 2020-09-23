import os
class Config(object):
    """docstring for ClassName"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'