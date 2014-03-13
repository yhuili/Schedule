import os

PWD = os.path.abspath(os.curdir)

DEBUG = True
#SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/sched.db'.format(PWD)
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/test'
SECRET_KEY = os.urandom(24)
SESSION_PROTECTION = 'strong'