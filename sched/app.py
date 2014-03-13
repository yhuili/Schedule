from flask import Flask
from flask import abort, jsonify, redirect, render_template, request, url_for
from flask.ext.login import LoginManager, current_user
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.sqlalchemy import SQLAlchemy
from sched import config, filters
from sched.forms import AppointmentForm, LoginForm, SignupForm
from sched.models import Base, Appointment, User

#create an instance of Flask, which is app
app = Flask(__name__)

#look for all UPPERCASE attributes on object config and load their values into the app config
app.config.from_object(config)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sched.db' #using sqlite as the database
#app.config['DEBUG'] = True

#using Flask-SQLAlchemy, connect to sqlite, set the default model class to the pure SQLAlchemy declarative Base class
db = SQLAlchemy(app)
db.models = Base

#load jinja filter
filters.init_app(app)

#track the current user with flask login
login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please login to check the appointments'

#setup logging for production.
if not app.debug:
    app.logger.setHandler(logging.StreamHandler()) #log to stderr.
    app.logger.setLevel(logging.INFO)


@login_manager.user_loader
def load_user(user_id):
	"""load a user with user_id"""
	return db.session.query(User).get(user_id)



#list all the appointment the user has
@app.route('/appointments/')
@login_required
def appointment_list():
    """Listing of all appointments we have"""
    appts = db.session.query(Appointment).filter_by(user_id=current_user.id).order_by(Appointment.start.asc()).all()
    return render_template('appointment/index.html', appts=appts)


#get the appointment by id
@app.route('/appointments/<int:appointment_id>/')
@login_required
def appointment_detail(appointment_id):
	"""write the information to HTML with the appointment by id"""
	appt = db.session.query(Appointment).get(appointment_id)
	if appt is None:
		abort(404)
	if appt.user_id != current_user.id:
		abort(403)
	return render_template('appointment/detail.html', appt=appt)


#get the appointment, and display a form to edit it
@app.route('/appointments/<int:appointment_id>/edit/', methods=['GET', 'POST'])
@login_required
def appointment_edit(appointment_id):
	"""write the information to HTML to edit the given appointment"""
	appt = db.session.query(Appointment).get(appointment_id)
	if appt is None:
		abort(404)
	if appt.user_id != current_user.id:
		abort(403)
	form = AppointmentForm(request.form, appt) ###try to use only one parameter request.form
	if request.method == 'POST' and form.validate():
		form.populate_obj(appt)
		db.session.commit()
		return redirect(url_for('appointment_detail', appointment_id=appt.id))
	return render_template('appointment/edit.html', form=form)


#create an appointment
@app.route('/appointments/create/', methods=['GET', 'POST'])
@login_required
def appointment_create():
	"""Populate the information from HTML to the form to create a new appointment"""
	form = AppointmentForm(request.form)
	if request.method == 'POST' and form.validate():
		appt = Appointment(user_id=current_user.id)
		form.populate_obj(appt)
		db.session.add(appt)
		db.session.commit()
		return redirect(url_for('appointment_list'))
	return render_template('appointment/edit.html', form=form)


#delete an appointment
@app.route('/appointments/<int:appointment_id>/delete/', methods=['DELETE'])
@login_required
def appointment_delete(appointment_id):
	"""delete record using HTTP delete, respond with JSON."""
	appt = db.session.query(Appointment).get(appointment_id)
	if appt is None:
		response = jsonify({'status': 'Not Found'})
		response.status = 404
		return response
	if appt.user_id != current_user.id:
		response = jsonify({'status': 'Forbidden'})
		response.status = 403
		return response
	db.session.delete(appt)
	db.session.commit()
	return jsonify({'status': 'OK'})


#error manipulation
@app.errorhandler(404)
def error_not_found(error):
    """Render a custom template when responding with 404 Not Found."""
    return render_template('error/not_found.html'), 404




#user manipulation, including sign up, login and logout
@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	form = SignupForm(request.form)
	error = None
	if request.method == 'GET':
		return render_template('user/signup.html', form=form)
	if request.method == 'POST' and form.validate():
		email = form.username.data.lower().strip()
		password = form.password.data.lower().strip()
		user, authenticated = User.authenticate(db.session.query, email, password)
		if user is None:
			user = User(email=email, password=password)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('appointment_list'))
		else:
			error = 'This email is already taken :('
	return render_template('user/signup.html', form=form, error=error)
			


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated():
		return redirect(url_for('appointment_list'))
	form = LoginForm(request.form)
	error = None
	if request.method == 'POST' and form.validate():
		email = form.username.data.lower().strip()
		password = form.password.data.lower().strip()
		user, authenticated = User.authenticate(db.session.query, email, password)
		if authenticated:
			login_user(user)
			return redirect(url_for('appointment_list'))
		else:
			error = 'Incorrect username or password, please try again :('
	return render_template('user/login.html', form=form, error=error)


@app.route('/logout/')
def logout():
	logout_user()
	return redirect(url_for('login'))







 
