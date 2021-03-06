import re
from unidecode import unidecode
import math
import random
import re
import sys
from hashlib import sha1

from flask import abort
from flask import render_template
from flask import request
from peewee import DoesNotExist
from peewee import ForeignKeyField
from peewee import Model
from peewee import SelectQuery
# from flask_peewee._compat import text_type

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'_'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))
	

def get_object_or_404(query_or_model, *query):
	if not isinstance(query_or_model, SelectQuery):
		query_or_model = query_or_model.select()
	try:
		return query_or_model.where(*query).get()
	except DoesNotExist:
		abort(404)

def object_list(template_name, qr, var_name='object_list', **kwargs):
	pq = PaginatedQuery(qr, kwargs.pop('paginate_by', 20))
	kwargs[var_name] = pq.get_list()
	return render_template(template_name, pagination=pq, page=pq.get_page(), **kwargs)


# class PaginatedQuery(object):
# 	page_var = 'page'
#
# 	def __init__(self, query_or_model, paginate_by):
# 		self.paginate_by = paginate_by
#
# 		if isinstance(query_or_model, SelectQuery):
# 			self.query = query_or_model
# 			self.model = self.query.model_class
# 		else:
# 			self.model = query_or_model
# 			self.query = self.model.select()
#
# 	def get_page(self):
# 		curr_page = request.args.get(self.page_var)
# 		if curr_page and curr_page.isdigit():
# 			return int(curr_page)
# 		return 1
#
# 	def get_pages(self):
# 		return int(math.ceil(float(self.query.count()) / self.paginate_by))
#
# 	def get_list(self):
# 		return self.query.paginate(self.get_page(), self.paginate_by)
#
#
# def get_next():
# 	if not request.query_string:
# 		return request.path
# 	return '%s?%s' % (request.path, request.query_string)
#
# def slugify(s):
# 	return re.sub('[^a-z0-9_\-]+', '-', s.lower())

def load_class(s):
	path, klass = s.rsplit('.', 1)
	__import__(path)
	mod = sys.modules[path]
	return getattr(mod, klass)

def get_dictionary_from_model(model, fields=None, exclude=None):
	model_class = type(model)
	data = {}

	fields = fields or {}
	exclude = exclude or {}
	curr_exclude = exclude.get(model_class, [])
	curr_fields = fields.get(model_class, model._meta.get_field_names())

	for field_name in curr_fields:
		if field_name in curr_exclude:
			continue
		field_obj = model_class._meta.fields[field_name]
		field_data = model._data.get(field_name)
		if isinstance(field_obj, ForeignKeyField) and field_data and field_obj.rel_model in fields:
			rel_obj = getattr(model, field_name)
			data[field_name] = get_dictionary_from_model(rel_obj, fields, exclude)
		else:
			data[field_name] = field_data
	return data

def get_model_from_dictionary(model, field_dict):
	if isinstance(model, Model):
		model_instance = model
		check_fks = True
	else:
		model_instance = model()
		check_fks = False
	models = [model_instance]
	for field_name, value in field_dict.items():
		field_obj = model._meta.fields[field_name]
		if isinstance(value, dict):
			rel_obj = field_obj.rel_model
			if check_fks:
				try:
					rel_obj = getattr(model, field_name)
				except field_obj.rel_model.DoesNotExist:
					pass
				if rel_obj is None:
					rel_obj = field_obj.rel_model
			rel_inst, rel_models = get_model_from_dictionary(rel_obj, value)
			models.extend(rel_models)
			setattr(model_instance, field_name, rel_inst)
		else:
			setattr(model_instance, field_name, field_obj.python_value(value))
	return model_instance, models

def path_to_models(model, path):
	accum = []
	if '__' in path:
		next, path = path.split('__')
	else:
		next, path = path, ''
	if next in model._meta.rel:
		field = model._meta.rel[next]
		accum.append(field.rel_model)
	else:
		raise AttributeError('%s has no related field named "%s"' % (model, next))
	if path:
		accum.extend(path_to_models(model, path))
	return accum


# borrowing these methods, slightly modified, from django.contrib.auth
def get_hexdigest(salt, raw_password):
	data = salt + raw_password
	return sha1(data.encode('utf8')).hexdigest()

# def make_password(raw_password):
# 	salt = get_hexdigest(text_type(random.random()), text_type(random.random()))[:5]
# 	hsh = get_hexdigest(salt, raw_password)
# 	return '%s$%s' % (salt, hsh)

def check_password(raw_password, enc_password):
	salt, hsh = enc_password.split('$', 1)
	return hsh == get_hexdigest(salt, raw_password)
	
	
## EXCEPTIONS
class ImproperlyConfigured(Exception):
	pass




class ReverseProxied(object):
	'''Wrap the application in this middleware and configure the 
	front-end server to add these headers, to let you quietly bind 
	this to a URL other than / and to an HTTP scheme that is 
	different than what is used locally.

	In nginx:
	location /myprefix {
		proxy_pass http://192.168.0.1:5001;
		proxy_set_header Host $host;
		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
		proxy_set_header X-Scheme $scheme;
		proxy_set_header X-Script-Name /myprefix;
		}

	:param app: the WSGI application
	'''
	def __init__(self, app):
		self.app = app

	def __call__(self, environ, start_response):
		script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
		if script_name:
			environ['SCRIPT_NAME'] = script_name
			path_info = environ['PATH_INFO']
			if path_info.startswith(script_name):
				environ['PATH_INFO'] = path_info[len(script_name):]

		scheme = environ.get('HTTP_X_SCHEME', '')
		if scheme:
			environ['wsgi.url_scheme'] = scheme
		return self.app(environ, start_response)





from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
				max_age=21600, attach_to_all=True,
				automatic_options=True):
	if methods is not None:
		methods = ', '.join(sorted(x.upper() for x in methods))
	if headers is not None and not isinstance(headers, basestring):
		headers = ', '.join(x.upper() for x in headers)
	if not isinstance(origin, basestring):
		origin = ', '.join(origin)
	if isinstance(max_age, timedelta):
		max_age = max_age.total_seconds()

	def get_methods():
		if methods is not None:
			return methods

		options_resp = current_app.make_default_options_response()
		return options_resp.headers['allow']

	def decorator(f):
		def wrapped_function(*args, **kwargs):
			if automatic_options and request.method == 'OPTIONS':
				resp = current_app.make_default_options_response()
			else:
				resp = make_response(f(*args, **kwargs))
			if not attach_to_all and request.method != 'OPTIONS':
				return resp

			h = resp.headers

			h['Access-Control-Allow-Origin'] = origin
			h['Access-Control-Allow-Methods'] = get_methods()
			h['Access-Control-Max-Age'] = str(max_age)
			if headers is not None:
				h['Access-Control-Allow-Headers'] = headers
			return resp

		f.provide_automatic_options = False
		return update_wrapper(wrapped_function, f)
	return decorator