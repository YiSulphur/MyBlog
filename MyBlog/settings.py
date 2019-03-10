import os
import sys
from MyBlog import app


SQLALCHEMY_TRACK_MODIFICATIONS = False


prefix = 'sqlite:///'

dev_db = prefix+os.path.join(os.path.dirname(app.root_path),'data.db')

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI',dev_db)

MYBLOG_THEMES = {'perfect_blue':'perfect_blue','black_swan':'black_swan'}
