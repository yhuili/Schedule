from jinja2 import Markup, evalcontextfilter, escape

#initialize a flask application with filters defined in the functions
def init_app(app):
	app.jinja_env.filters['date'] = do_date
	app.jinja_env.filters['datetime'] = do_datetime
	app.jinja_env.filters['do_duration'] = do_duration
	app.jinja_env.filters['nl2br'] = evalcontextfilter(do_nl2br)


def do_date(dt, format=None):
	"""Jinja template filter to format a date object"""
	if dt is None:
		return ''
	if format is None:
		formatted = dt.strftime('%Y-%m-%d - %A')
	else:
		formatted = dt.strftime(format)
	return formatted


def do_datetime(dt, format=None):
	"""Jinja template filter to format a datetime object"""
	if dt is None:
		return ''
	if format is None:
		formatted_date = dt.strftime('%Y-%m-%d - %A')
		formatted_time = dt.strftime('%I:%M%p').lstrip('0').lower()
		formatted = '%s at %s' % (formatted_date, formatted_time)
	else:
		formatted = dt.strftime(format)
	return formatted


def do_duration(duration_in_seconds):
	"""Jinja template filter to format a duration object"""
	minitues, seconds = divmod(duration_in_seconds, 60)
	hours, minitues = divmod(minitues, 60)
	days, hours = divmod(hours, 24)
	duration_result = []
	
	if days > 1:
		duration_result.append('{days} days') #try to change {days} to {d}, and days=days to d=days
	elif days:
		duration_result.append('{days} day')
	if hours > 1:
		duration_result.append('{hours} hours')
	elif hours:
		duration_result.append('{hours} hour')
	if minitues > 1:
		duration_result.append('{minitues} minitues')
	elif minitues:
		duration_result.append('{minitues} minitue')
	if seconds > 1:
		duration_result.append('{seconds} seconds')
	elif seconds:
		duration_result.append('{seconds} second')

	formatted = ', '.join(duration_result)
	return formatted.format(days=days, hours=hours, minitues=minitues, seconds=seconds)


def do_nl2br(contex, value):
	"""Jinja template filter to transform new line to <br /> in HTML"""
	formatted = u'<br />'.join(escape(value).split('\n'))
	if contex.autoescape:
		formatted = Markup(formatted)
	return formatted











