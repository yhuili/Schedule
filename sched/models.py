from datetime import datetime
from sqlalchemy import Column, ForeignKey, Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import synonym, relationship
from sqlalchemy.ext.declarative import declarative_base
from werkzeug import check_password_hash, generate_password_hash


#Base is the sqlalchemy base class to store data
Base = declarative_base()


class User(Base):
	"""A user to login, with credentials and authentication"""
	__tablename__ = 'user' #declare the table name
	
	id = Column(Integer, primary_key=True)
	created = Column(DateTime, default=datetime.now)
	modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	name = Column('name', String(200))
	email = Column(String, unique=True, nullable=False)
	active = Column(Boolean, default=True)
	_password = Column('password', String(100))

	def __init__(self, email, password):
		self.email = email
		self.password = password
		
	#define functions to deal with password
	def _get_password(self):
		return self._password

	def _set_password(self, password):
		if password:
			password = password.strip()
		self._password = generate_password_hash(password)

	password_descriptor = property(_get_password, _set_password)
	password = synonym('_password', descriptor=password_descriptor)

	def check_password(self, password):
		if self.password is None:
			return False
		password = password.strip()
		if not password:
			return False
		return check_password_hash(self.password, password)

	@classmethod
	def authenticate(cls, query, email, password):
		email = email.strip().lower()
		user = query(cls).filter(cls.email==email).first()
		if user is None:
			return None, False
		if not user.active:
			return user, False
		return user, user.check_password(password)


	def get_id(self):
		return str(self.id)

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def __repr__(self):
		return u'<{self.__class__.__name__}:{self.id}>'.format(self=self)


#inherit the base class in Flask
class Appointment(Base):
	"""An appointment on the calendar. Modeling an Appointment class which maps objects to an Appointment table"""
	__tablename__ = 'appointment' #declare the table name

	id = Column(Integer, primary_key=True) #id for appointment
	created = Column(DateTime, default=datetime.now) #time stamp for appointment created
	modified = Column(DateTime, default=datetime.now, onupdate=datetime.now) #time stamp for appointment modified
	title = Column(String(255))
	start = Column(DateTime, nullable=False)
	end = Column(DateTime, nullable=False)
	allday = Column(Boolean, default=False)
	location = Column(String(255))
	description = Column(Text)

	user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
	user = relationship(User, lazy='joined', join_depth=1)

	@property
	def duration(self):
		delta = self.end - self.start
		return delta.days * 24 * 60 * 60 + delta.seconds

	#override the __repr__ method
	def __repr__(self):
		return u'<{self.__class__.__name__}:{self.id}>'.format(self=self)



if __name__ == '__main__':
	from datetime import timedelta
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	#using the SQLite database in memory, which only exists for the duration of Python's process execution.
	engine = create_engine('sqlite://', echo=True)
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()
	
	#create fake db content to test the model class connecting to the database
	user = User(name='Hui Li', email='hli997@usc.edu', password='123')
	session.add(user)
	session.commit()

	now = datetime.now()
	session.add(Appointment(
		title = 'Important Interview', 
		start = now+timedelta(days=3), 
		end = now+timedelta(days=3, seconds=3600),
		allday = False,
		location = 'Universal Studio',
		user_id = user.id))
	session.commit()

	session.add(Appointment(
		title = 'Past Interview', 
		start = now-timedelta(days=7), 
		end = now-timedelta(days=7, seconds=3600),
		allday = False,
		location = 'Universal Studio',
		user_id = user.id))
	session.commit()

	session.add(Appointment(
		title = 'Follow Up', 
		start = now-timedelta(days=4), 
		end = now-timedelta(days=4, seconds=3600),
		allday = False,
		location = 'Universal Studio',
		user_id = user.id))
	session.commit()

	session.add(Appointment(
		title = 'Day Off', 
		start = now+timedelta(days=5), 
		end = now+timedelta(days=5),
		allday = True,
		user_id = user.id))
	session.commit()
	
	#create instance
	appt = Appointment(
		title = 'My Appointment', 
		start = now,
		end = now+timedelta(seconds=1800),
		allday = False,
		user_id = user.id)
	session.add(appt)
	session.commit()
	
	#update instace
	appt.title = 'My Appointment 2'
	session.commit()
	
	# #delete
	# session.delete(appt)
	# session.commit()

	# #create fake queries to test the model class connecting to the database
	# #get an appoitment by id
	# appt = session.query(Appointment).get(1)

	# #get all appointments
	# appts = session.query(Appointment).all()

	# #get all appoinments before right now, after right now
	# appts = session.query(Appointment).filter(Appointment.start < datetime.now()).all()
	# appts = session.query(Appointment).filter(Appointment.start >= datetime.now()).all()

	# #get all appoinments before a certain date.
	# appts = session.query(Appointment).filter(Appointment.start <= datetime(2014, 3, 9)).all()

	# #get the first appointment matching the filter query
	# appt = session.query(Appointment).filter(Appointment.start <= datetime(2014, 3, 9)).first()





