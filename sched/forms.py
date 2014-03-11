from __future__ import print_function
from wtforms import Form, BooleanField, DateTimeField
from wtforms import TextAreaField, TextField, PasswordField
from wtforms.validators import Length, required
from werkzeug.datastructures import ImmutableMultiDict as multidict


class AppointmentForm(Form):
	"""HTML form generation and validation of form data, display a form in HTML"""
	title = TextField('Title', [Length(max=255)]) #the second parameter Length is used to ensure an input of maximum of 255 chars
	start = DateTimeField('Start', [required()])
	end = DateTimeField('End')
	allday = BooleanField('All Day')
	location = TextField('Location', [Length(max=255)])
	description = TextAreaField('Description')

class LoginForm(Form):
	"""HTML form generation and validation of form data, display a form in HTML"""
	username = TextField('username', [required()])
	password = PasswordField('password', [required()])	


if __name__ == '__main__':
	form = AppointmentForm()
	# print('Here is how a form field displays:')
	# print(form.title.label)
	# print(form.title)
	data = multidict([('title', 'Hello Form!')])
	form = AppointmentForm(data)
	print('Here is validation...')
	print('Does it validate:{}'.format(form.validate()))
	print('There is an error attached to the field...')
	print('form.start.errors:{}'.format(form.start.errors))