import os
import sys
import tempfile

pwd = os.path.abspath(os.path.dirname(__file__))
project = os.path.basename(pwd)
full_path = pwd.strip(project)


try:
    from project import app
except ImportError:
    sys.path.append(full_path)
    from project import app


def before_feature(context, feature):
    app.config['TESTING'] = True
    context.client = app.test_client()
    

def after_feature(context, feature):
    pass
