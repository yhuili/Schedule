import os

#Get the current working directory to place sched.db during development.
#In production, use absolute paths or a database management system.
PWD = os.path.abspath(os.curdir)

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/sched.db'.format(PWD)
SECRET_KEY = os.urandom(24)
SESSION_PROTECTION = 'strong'