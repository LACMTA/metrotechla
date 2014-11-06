import datetime
import simplejson as json
from flask import (
	Flask,
	# Blueprint,
	Response,
	session,
	get_flashed_messages,
	jsonify,
	request,
	render_template,
	redirect,
	g,
)
from peewee import (
	Model, 
	CharField, 
	# BlobField,
	BooleanField, 
	TextField, 
	FloatField,
	IntegerField,
	TextField,
	# UUIDField,
	ForeignKeyField,
	DateTimeField,
	SqliteDatabase,
	)
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.peewee import ModelView
from flask.ext.security import (
	Security,
	PeeweeUserDatastore,
	UserMixin, 
	RoleMixin, 
	login_required,
	)
from flask_security.core import current_user
from flask_security.utils import logout_user
from flask_restful_swagger import swagger

from utils import (
	slugify, 
	ReverseProxied,
	# crossdomain,
	)

db = SqliteDatabase('leaderboard.sqlite', check_same_thread=False)

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.wsgi_app = ReverseProxied(app.wsgi_app)

# Flask-Mail
# from flask_mail import Mail
# mail = Mail(app)

class BaseModel(Model):
	class Meta:
		database = db

class Role(BaseModel, RoleMixin):
	name = CharField(unique=True)
	description = TextField(null=True)

	def __repr__(self):
		return '<User %r>' % (self.name)

	def __unicode__(self):
		return self.name

class User(BaseModel, UserMixin):
	email = TextField()
	password = TextField(default='MetroTechLA')
	active = BooleanField(default=True)
	confirmed_at = DateTimeField(null=True)

	def has_voted(self,sessn):
		print "get vote count for session %s and participant %s" %(sessn,self)
		vtcount = Vote.select().where(Vote.sessn==sessn,Vote.participant==self).count()
		if vtcount>0:
			return 1
		else:
			return 0

	@property
	def myvotes(self):
		# vtlist = []
		# for v in Vote.select().where(Vote.participant==self):
		# 	myd = {'track':str(v.sessn.track),'session':str(v.sessn),'presentation':str(v.presentation),'vendor':str(v.presentation.vendor)}
		# 	vtlist.append(myd)
		# return json.dumps(vtlist)
		return 1

	@property
	def admin(self):
		return self.has_role('admin')

	@property
	def is_admin(self):
		return self.has_role('admin')

	def __repr__(self):
		return '<User %r>' % (self.email)

	def __unicode__(self):
		return self.email

class UserRoles(BaseModel):
	# Because peewee does not come with built-in many-to-many
	# relationships, we need this intermediary class to link
	# user to roles.
	user = ForeignKeyField(User, related_name='roles')
	role = ForeignKeyField(Role, related_name='users')
	name = property(lambda self: self.role.name)
	description = property(lambda self: self.role.description)

	def __repr__(self):
		return '<User %r, Role %r>' % (self.user.email, self.role.name)

	def __unicode__(self):
		return '(%r,%r)' % (self.user.email, self.role.name)


class Track(BaseModel):
	title = CharField(default='Multi-Modal Integration',max_length=50)
	description = TextField(default="is...")
	active = BooleanField(default=True)
	slug = CharField(default='',max_length=50)
	
	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super(Track, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title
		
	def __repr__(self):
		return '<Track %r>' % (self.title)

class Sessn(BaseModel):
	title = CharField(default='Bike Sharing',max_length=50)
	description = TextField(default="is...")
	track = ForeignKeyField(Track, related_name='session')
	active = BooleanField(default=True)
	slug = CharField(default='',max_length=50)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super(Sessn, self).save(*args, **kwargs)

	def get_scores(self):
		scorelist = []
		for p in Presentation.select().where(Presentation.sessn==self):
			vendr = p.vendor
			vendortitle = vendr.__unicode__()
			vendorct = Vote.select().where(Vote.vendor==vendr,Vote.sessn==self).count()
			scorelist.append({'vendor':vendortitle,'score':vendorct})
		return json.dumps({'sessn':self.__unicode__(),'scores':scorelist})

	def __unicode__(self):
		return self.title

	def __repr__(self):
		return '<Sessn %r>' % (self.title)

class Vendor(BaseModel):
	title = CharField(default='Bikr',max_length=50)
	description = TextField(default="are...")
	active = BooleanField(default=True)

	def get_score(self):
		return Vote.select().where(vendor=self).count()

	def __unicode__(self):
		return self.title

@swagger.model
class Presentation(BaseModel):
	title = CharField(default='Social Bicycles',max_length=50)
	sessn = ForeignKeyField(Sessn, related_name='presentations')
	vendor = ForeignKeyField(Vendor, related_name='presentations')
	description = TextField(default="is...")
	active = BooleanField(default=True)
	score = IntegerField(default=0)
	slug = CharField(default='',max_length=50)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		return super(Presentation, self).save(*args, **kwargs)

	def get_score(self):
		score = Vote.select().where(Vote.presentation==self).count()
		self.score = score
		return self.score

	def __unicode__(self):
		return self.title

	def __repr__(self):
		return '<Presentation %r>' % (self.title)


class Vote(BaseModel):
	sessn = ForeignKeyField(Sessn, related_name='sessionvote')
	presentation = ForeignKeyField(Presentation, related_name='presentationvote')
	participant = ForeignKeyField(User, related_name='participantvote')
	timestamp = DateTimeField(default=datetime.datetime.now)

	# def create(self,sessn,presentation,participant):
	# 	print "has %s voted for presentation %s in session %s ?" %(participant,presentation,sessn)
	# 	# super(Vote, self).__init__()
	# 	super(Vote, self).save(*args, **kwargs)
	# 	if not participant.has_voted(sessn):
	# 		print "Record this vote"
	# 		self.sessn = sessn
	# 		self.presentation = presentation
	# 		self.participant = participant
	# 	else:
	# 		# myvote = Vote.select().where(Vote.sessn==sessn,Vote.participant==participant).get()
	# 		# OR: we could also change the vote here:
	# 		print "ok, we changed %s's vote in session %s to presentation %s" %(participant,sessn,presentation)
	# 		self.sessn = sessn
	# 		self.presentation = presentation
	# 		self.participant = participant

	def __init__(self,sessn,presentation,participant):
		print "has %s voted for presentation %s in session %s ?" %(participant,presentation,sessn)
		super(Vote, self).__init__()
		if not participant.has_voted(sessn):
			print "Record this vote"
			self.sessn = sessn
			self.presentation = presentation
			self.participant = participant
		else:
			# myvote = Vote.select().where(Vote.sessn==sessn,Vote.participant==participant).get()
			# OR: we could also change the vote here:
			print "ok, we changed %s's vote in session %s to presentation %s" %(participant,sessn,presentation)
			self.sessn = sessn
			self.presentation = presentation
			self.participant = participant

	@property
	def vendor(self):
		return 	self.presentation.vendor

	def __unicode__(self):
		return '%s voted for presentation %s in session %s' % (self.participant.__unicode__(), self.presentation, self.sessn)

	def __repr__(self):
		return '<Vote User %r, Presentation %r>' % (self.participant, self.presentation)


# Setup Flask-Security
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore)

# Create a user to test with
# @app.before_first_request
# def create_user():
# 	for Model in (Role, User, UserRoles):
# 		Model.drop_table(fail_silently=True)
# 		Model.create_table(fail_silently=True)
# 	user_datastore.create_user(email='rotten@metro.net', password='rotten@metro.net')


## LOAD DATA
# @app.before_first_request
def load_data():
	admin=User.create(email='goodwind@metro.net', password='admin')
	
	admin_role=Role(name='admin',description='')
	admin_role.save()
	participant_role=Role(name='participant',description='')
	participant_role.save()
	
	admin_admin=UserRoles(user=admin,role=admin_role)
	admin_admin.save()
	
	john=User.create(email=u'john@metro.net',password=u'john@metro.net')
	paul=User.create(email=u'paul@metro.net',password=u'paul@metro.net')
	george=User.create(email=u'george@metro.net',password=u'george@metro.net')
	ringo=User.create(email=u'ringo@metro.net',password=u'ringo@metro.net')

	john_participant=UserRoles(user=john,role=participant_role)
	john_participant.save()
	paul_participant=UserRoles(user=paul,role=participant_role)
	paul_participant.save()
	george_participant=UserRoles(user=george,role=participant_role)
	george_participant.save()
	ringo_participant=UserRoles(user=ringo,role=participant_role)
	ringo_participant.save()

	track_m=Track.create(title=u'Multi-Modal Integration')
	track_f=Track.create(title=u'Station of the Future')
	track_n=Track.create(title=u'Next Generation Trip Planning and Fare Payments')

	sessn_bs=Sessn.create(title=u'Bike Sharing',track=track_m)
	sessn_cs=Sessn.create(title=u'Car Sharing',track=track_m)
	sessn_av=Sessn.create(title=u'Autonomous Vehicles',track=track_m)
	sessn_va=Sessn.create(title=u'Virtual Agents/Kiosks/Wayfinding',track=track_f)
	sessn_cse=Sessn.create(title=u'Concierge Services',track=track_f)
	sessn_wc=Sessn.create(title=u'Wireless Connectivity',track=track_f)
	sessn_st=Sessn.create(title=u'Smart Trip Planning',track=track_n)
	sessn_ga=Sessn.create(title=u'Gamification and Loyalty Programs',track=track_n)
	sessn_ng=Sessn.create(title=u'Next Generation Fare Payments',track=track_n)

	vendor_ac=Vendor.create(title=u'Accenture')
	vendor_an=Vendor.create(title=u'Aruba Networks')
	vendor_ca=Vendor.create(title=u'CHK America')
	vendor_cg=Vendor.create(title=u'Control Group')
	vendor_cp=Vendor.create(title=u'CradlePoint')
	vendor_cs=Vendor.create(title=u'Cambridge Systematics')
	vendor_gg=Vendor.create(title=u'Giro')
	vendor_gv=Vendor.create(title=u'Global VP')
	vendor_ks=Vendor.create(title=u'Kaonsoft')
	vendor_sb=Vendor.create(title=u'Social Bicycles')
	vendor_sp=Vendor.create(title=u'SinglePoint')
	vendor_tc=Vendor.create(title=u'TransitVue Communications')
	vendor_tg=Vendor.create(title=u'Trapeze Group')
	vendor_tk=Vendor.create(title=u'T-Kartor USA')
	vendor_xt=Vendor.create(title=u'Xerox Transportation Services')

	pres_av_ac=Presentation.create(title=u'accenture on autonomous vehicles',sessn=sessn_av,vendor=vendor_ac)
	pres_av_cg=Presentation.create(title=u'control group autonomous',sessn=sessn_av,vendor=vendor_cg)
	pres_bs_cg=Presentation.create(title=u'control group on bike sharing',sessn=sessn_bs,vendor=vendor_cg)
	pres_bs_sb=Presentation.create(title=u'bicycles are social',sessn=sessn_bs,vendor=vendor_sb)
	pres_cse_ac=Presentation.create(title=u'accenture on concierge servs',sessn=sessn_cse,vendor=vendor_ac)
	pres_cse_cg=Presentation.create(title=u'control group concierge',sessn=sessn_cse,vendor=vendor_cg)
	pres_cs_cg=Presentation.create(title=u'control group on car sharing',sessn=sessn_cs,vendor=vendor_cg)
	pres_cs_cs=Presentation.create(title=u'cambridge systematics on car sharing',sessn=sessn_cs,vendor=vendor_cs)
	pres_ga_ac=Presentation.create(title=u'accenture on gamification',sessn=sessn_ga,vendor=vendor_ac)
	pres_ng_ac=Presentation.create(title=u'accenture on next gen fare paytments',sessn=sessn_ng,vendor=vendor_ac)
	pres_ng_cg=Presentation.create(title=u'control group on next gen fare payments',sessn=sessn_ng,vendor=vendor_cg)
	pres_st_ac=Presentation.create(title=u'accenture on smart trips',sessn=sessn_st,vendor=vendor_ac)
	pres_st_cg=Presentation.create(title=u'control group on smart trips',sessn=sessn_st,vendor=vendor_cg)
	pres_wc_cg=Presentation.create(title=u'control group wireless connectivity',sessn=sessn_wc,vendor=vendor_cg)

	vote_j_bssb_sb=Vote.create(sessn=sessn_bs,presentation=pres_bs_sb,participant=john)
	vote_p_bssb_sb=Vote.create(sessn=sessn_bs,presentation=pres_bs_sb,participant=paul)
	vote_g_bssb_cg=Vote.create(sessn=sessn_bs,presentation=pres_bs_cg,participant=george)
	vote_r_bssb_cg=Vote.create(sessn=sessn_bs,presentation=pres_bs_cg,participant=ringo)

	vote_j_cscs_cg=Vote.create(sessn=sessn_cs,presentation=pres_cs_cg,participant=john)
	vote_p_cscs_cg=Vote.create(sessn=sessn_cs,presentation=pres_cs_cg,participant=paul)
	vote_g_cscg_cs=Vote.create(sessn=sessn_cs,presentation=pres_cs_cs,participant=george)
	vote_r_cscs_cg=Vote.create(sessn=sessn_cs,presentation=pres_cs_cg,participant=ringo)

	vote_j_avac_cg=Vote.create(sessn=sessn_av,presentation=pres_av_cg,participant=john)
	vote_p_avac_cg=Vote.create(sessn=sessn_av,presentation=pres_av_cg,participant=paul)
	vote_g_avac_ac=Vote.create(sessn=sessn_av,presentation=pres_av_ac,participant=george)
	vote_r_avac_cg=Vote.create(sessn=sessn_av,presentation=pres_av_cg,participant=ringo)

	# this should reset John's vote
	vote_j_bssb_sb=Vote.create(sessn=sessn_bs,presentation=pres_bs_cg,participant=john)

class UserAdmin(ModelView):
	# Visible columns in the list view
	column_exclude_list = ['password']

class VoteView(ModelView):
	# Override displayed fields
	column_list = ('sessn', 'presentation', 'participant','timestamp')

class MyHomeView(AdminIndexView):
	@expose('/')
	# @requires_admin
	def index(self):
		printme = ""
		for t in Track.select():
			printme = printme + "<H1>%s</H1>" %(t.title)
			for s in Sessn.select().where(Sessn.track==t):
				printme = printme + "<H2>%s</H2>" %(s.title)
				for p in Presentation.select().where(Presentation.sessn==s):
					vendr = p.vendor
					vendortitle = vendr.__unicode__()
					vendorct = Vote.select().where(Vote.presentation==p,Vote.sessn==s).count()
					printme = printme + "<H4>%s: <span id='result_%s'>%d</span></H4><a id='myLink' href='#' onclick='addVote(%s);return false;'>[vote]</a>" %(vendortitle,p.id,vendorct,p.id)
		return self.render('adminhome.html', leaderb=printme)


# flask admin
admin = Admin(app, name='MetroTechLA',index_view=MyHomeView())
admin.add_view(UserAdmin(User))
admin.add_view(ModelView(Role))
admin.add_view(ModelView(UserRoles))
admin.add_view(ModelView(Track))
admin.add_view(ModelView(Sessn))
admin.add_view(ModelView(Vendor))
admin.add_view(ModelView(Presentation))
# admin.add_view(ModelView(Vote))
admin.add_view(VoteView(Vote))


# Flask restful
from flask.ext.restful import reqparse, abort, Api, Resource

# api = restful.Api(app)
###################################
# Wrap the Api with swagger.docs. It is a thin wrapper around the Api class that adds 
# some swagger smarts
api = swagger.docs(Api(app), apiVersion='0.1')
###################################


class HelloWorld(Resource):
	# @login_required
	def get(self):
		return {'hello': 'world'}

api.add_resource(HelloWorld, '/api/')

def abort_if_presentation_doesnt_exist(presentation_id):
	if not Presentation.select().where(Presentation.id==presentation_id).count():
		abort(404, message="Presentation {} doesn't exist".format(presentation_id))

parser = reqparse.RequestParser()


# Presentation
#   single presentation: edit, delete
class APresentation(Resource):
	"Describing elephants"
	@swagger.operation(
		notes='some really good notes',
		responseClass=Presentation.__name__,
		nickname='upload',
		parameters=[
			{
				"name": "body",
				"description": "blueprint object that needs to be added. YAML.",
				"required": True,
				"allowMultiple": False,
				"dataType": Presentation.__name__,
				"paramType": "body"
			}
			],
			responseMessages=[
			{
				"code": 201,
				"message": "Created. The URL of the created blueprint should be in the Location header"
			},
			{
				"code": 405,
				"message": "Invalid input"
			}
		]
	)

	@login_required
	def get(self, presentation_id):
		abort_if_presentation_doesnt_exist(presentation_id)
		l = Presentation.get(Presentation.id==presentation_id)
		return {
				'title':l.title,
				'presentation_id':l.id,
				'score':l.get_score(),
				'session':l.sessn.title,
				'vendor':l.vendor.title,
				'slug':l.slug,
				'email':current_user.email
			}

	@login_required
	# @crossdomain(origin='*')
	def put(self, presentation_id):
		msg=""
		abort_if_presentation_doesnt_exist(presentation_id)
		user = g.get('user', None)
		l = Presentation.get(Presentation.id==presentation_id)
		# parser.add_argument('email', type=str)
		# args = parser.parse_args()
		try:
			participnt = User.get(User.email==current_user.email)
			msg=msg+"got the participant... "
			if participnt.has_voted(l.sessn):
				# curvote = Vote.get(Vote.sessn==l.sessn,Vote.participant==participnt)
				# print "curvote is %s" %curvote
				# curvote.score = curvote.score-1
				msg=msg+"and he voted for presentation %s in session %s. Update!" %(l.sessn,l)
				bluh="Vote switched! You can switch votes again at any time by refreshing this page."
				q=Vote.update(presentation=l).where(Vote.sessn==l.sessn,Vote.participant==participnt)
				q.execute()
			else:
				msg=msg+"he hasn't voted in session %s. create(sessn=%s,presentation=%s,participant=%s)" %(l.sessn,l.sessn,l,participnt)
				Vote.create(sessn=l.sessn,presentation=l,participant=participnt)
				bluh="Thanks for voting! You can switch votes at any time by refreshing this page."
		except:
			abort(404, message="Sorry {} something went wrong".format(current_user.email))
		return {
			'title':l.title,
			'presentation_id':l.id,
			'score':l.get_score(),
			'session':l.sessn.title,
			'vendor':l.vendor.title,
			'msg':msg,
			'bluh':bluh,
			'email':current_user.email,
		},201



	# def delete(self, todo_id):
	# 	abort_if_presentation_doesnt_exist(todo_id)
	# 	del Presentation[presentation_id]
	# 	return '', 204
	#
	# def put(self, todo_id):
	# 	args = parser.parse_args()
	# 	task = {'task': args['task']}
	# 	TODOS[todo_id] = task
	# 	return task, 201

# TrackList
#   shows a list of all tracks
class TrackList(Resource):
	def get(self):
		mps = Track.select()
		return [
			{
				'title':l.title,
				'track_id':l.id,
				'slug':l.slug,
				'description':l.description,
			} 
			for l in mps]

# SessionList
#   shows a list of all tracks
class SessnList(Resource):
	def get(self,track_slug='multi_modal_integration'):
		if track_slug:
			tr=Track.get(Track.slug==track_slug)
			mps = Sessn.select().where(Sessn.track==tr)
			return [
				{
					'title':l.title,
					'session_id':l.id,
					'slug':l.slug,
					'track':str(l.track.title),
					'track_id':l.track.id,
					'description':l.description,
				} 
				for l in mps]
		else:
			mps = Sessn.select()
			return [
				{
					'title':l.title,
					'session_id':l.id,
					'slug':l.slug,
					'track':str(l.track.title),
					'track_id':l.track.id,
					'description':l.description,
				} 
				for l in mps]

# ASessn
#   shows a list of all sessions by track
class ASessn(Resource):
	def get(self, track_slug):
		if track_slug:
			tr=Track.get(Track.slug==track_slug)
		return {
				'title':tr.title,
				'slug':tr.slug,
				'track':str(tr.title),
				'track_id':tr.id,
				'description':tr.description,
			}


# ATrackSessn
#   shows a list of all sessions by track
class ATrackSessn(Resource):
	def get(self, track_slug,sessn_slug):
		if track_slug:
			tr=Track.get(Track.slug==track_slug)
			se=Sessn.get(Sessn.slug==sessn_slug)
			mps = Presentation.select().where(Presentation.sessn==se)
			mps_structure = [
						{
							'title':l.title,
							'presentation_id':l.id,
							'score':l.get_score(),
							'session':l.sessn.title,
							'vendor':l.vendor.title,
							'slug':l.slug,
							'url':'/api/presentation/%s/' %(l.id)
						} 
						for l in mps]
		return {
				'title':se.title,
				'session_id':se.id,
				'slug':se.slug,
				'track':str(se.track.title),
				'track_id':se.track.id,
				'description':se.description,
				'presentations':mps_structure,
			}


# PresentationList
#   shows a list of all presentations
class PresentationList(Resource):
	def get(self):
		mps = Presentation.select()
		return [
			{
				'title':l.title,
				'presentation_id':l.id,
				'score':l.get_score(),
				'session':l.sessn.title,
				'vendor':l.vendor.title,
				'slug':l.slug,
				'slug':l.slug,
			} 
			for l in mps]

##
## Actually setup the Api resource routing here
##
api.add_resource(TrackList, '/api/track/')
api.add_resource(ASessn, '/api/track/<string:track_slug>/')
api.add_resource(SessnList, '/api/track/<string:track_slug>/session/')
api.add_resource(ATrackSessn, '/api/track/<string:track_slug>/session/<string:sessn_slug>/')
api.add_resource(PresentationList, '/api/presentation/')
api.add_resource(APresentation, '/api/presentation/<string:presentation_id>/')


# Views
@app.route('/')
@login_required
def home():
	printme = ""
	for t in Track.select():
		printme = printme + "<H1>%s</H1>" %(t.title)
		for s in Sessn.select().where(Sessn.track==t):
			printme = printme + "<H2>%s</H2>" %(s.title)
			for p in Presentation.select().where(Presentation.sessn==s):
				vendr = p.vendor
				vendortitle = vendr.__unicode__()
				vendorct = Vote.select().where(Vote.presentation==p,Vote.sessn==s).count()
				printme = printme + "<H4>%s: %d</H4>" %(vendortitle,vendorct)
	return render_template('index.html', leaderb=printme, current_user=current_user)


@app.route('/flask')
@login_required
def hello_world():
	return 'This comes from Flask ^_^'

@app.route('/vote')
@login_required
def vote_test():
	return render_template('vote.html', current_user=current_user)

@app.route('/result')
def result_test():
	return render_template('result.html', current_user=current_user)

@app.route('/register', methods=['GET'])
def register():
	return render_template('security/register_user.html')


if __name__ == '__main__':
	import logging
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)

	User.create_table(fail_silently=True)
	Role.create_table(fail_silently=True)
	UserRoles.create_table(fail_silently=True)
	Track.create_table(fail_silently=True)
	Sessn.create_table(fail_silently=True)
	Presentation.create_table(fail_silently=True)
	Vendor.create_table(fail_silently=True)
	Vote.create_table(fail_silently=True)

	# install some data
	# why does this fail?
	# load_data()

	app.run()
	
