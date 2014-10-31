"""
	email = TextField()
	password = TextField()
	active = BooleanField(default=True)
	confirmed_at = DateTimeField(null=True)
	first_name = TextField(null=True)
	last_name = TextField(null=True)
	affiliation = TextField(null=True)

f="/Users/admin/Documents/metrotechla.csv"
input_file = csv.DictReader(open(f))

for row in input_file:
	print "me=User.create(email='%s', password='%s',first_name='%s',last_name='%s',affiliation='%s')
UserRoles.create(user=me,role=participant_role)" %(row["Email"],row["Email"],row["First Name"],row["Last Name"],row["Company"],)

"""



# ROLES
admin_role=Role.create(name='admin',description='')
participant_role=Role.create(name='participant',description='')

# ADMINS
admin=User.create(email='goodwind@metro.net', password='admin',first_name='Doug',last_name='Admin',affiliation='Metro')
UserRoles.create(user=admin,role=admin_role)

# TEST PARTICIPANTS
john = User.create(email=u'john@metro.net',password=u'john@metro.net',first_name='John',last_name='L',affiliation='Metro')
UserRoles.create(user=john,role=participant_role)

paul=User.create(email=u'paul@metro.net',password=u'paul@metro.net',first_name='Paul',last_name='M',affiliation='Metro')
UserRoles.create(user=paul,role=participant_role)

george=User.create(email=u'george@metro.net',password=u'george@metro.net',first_name='George',last_name='H',affiliation='Metro')
UserRoles.create(user=george,role=participant_role)

ringo=User.create(email=u'ringo@metro.net',password=u'ringo@metro.net',first_name='Ringo',last_name='S',affiliation='Metro')
UserRoles.create(user=ringo,role=participant_role)

# TRACKS
track_m=Track.create(title=u'Multi-Modal Integration')
track_f=Track.create(title=u'Station of the Future')
track_n=Track.create(title=u'Next Generation Trip Planning and Fare Payments')

# SESSIONS
sessn_bs=Sessn.create(title=u'Bike Sharing',track=track_m)
sessn_cs=Sessn.create(title=u'Car Sharing',track=track_m)
sessn_av=Sessn.create(title=u'Autonomous Vehicles',track=track_m)
sessn_va=Sessn.create(title=u'Virtual Agents/Kiosks/Wayfinding',track=track_f)
sessn_cse=Sessn.create(title=u'Concierge Services',track=track_f)
sessn_wc=Sessn.create(title=u'Wireless Connectivity',track=track_f)
sessn_st=Sessn.create(title=u'Smart Trip Planning',track=track_n)
sessn_ga=Sessn.create(title=u'Gamification and Loyalty Programs',track=track_n)
sessn_ng=Sessn.create(title=u'Next Generation Fare Payments',track=track_n)

# VENDORS
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

# PRESENTATIONS
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

# VOTES
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

# PARTICIPANTS
me=User.create(email='adams.1170@gmail.com', password='adams.1170@gmail.com',first_name='Brendan',last_name='Adams',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='aaguilar@santa-clarita.com', password='aaguilar@santa-clarita.com',first_name='Adrian',last_name='Aguilar',affiliation='City of Santa Clarita')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='MAlRawi@bos.lacounty.gov', password='MAlRawi@bos.lacounty.gov',first_name='Mohammed',last_name='Al Rawi',affiliation='Office of Supervisor Ridley-Thomas')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='alegree@metro.net', password='alegree@metro.net',first_name='Ed',last_name='Alegre',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='diane.amaya@redondo.org', password='diane.amaya@redondo.org',first_name='Diane',last_name='Amaya',affiliation='City of Redondo Beach')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='aronsohna@scrra.net', password='aronsohna@scrra.net',first_name='Andrew',last_name='Aronsohn',affiliation='Metrolink')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='astredop@metro.net', password='astredop@metro.net',first_name='Patrick',last_name='Astredo',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='sbaghdanian@glendaleca.gov', password='sbaghdanian@glendaleca.gov',first_name='Silva',last_name='Baghdanian',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dbarnes@foothlltransit.org', password='dbarnes@foothlltransit.org',first_name='Doran',last_name='Barnes',affiliation='Foothill Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='alibartle@gmail.com', password='alibartle@gmail.com',first_name='Alicen',last_name='Bartle',affiliation='Rising Realty Partners')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='todd.borowski@kaonsoft.com', password='todd.borowski@kaonsoft.com',first_name='Todd',last_name='Borowski',affiliation='Kaonsoft')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='chris.boult@greyhound.com', password='chris.boult@greyhound.com',first_name='Chris',last_name='Boult',affiliation='Greyhound')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='brooky489@gmail.com', password='brooky489@gmail.com',first_name='Alexis',last_name='Brooks',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jeffmbrooks@gmail.com', password='jeffmbrooks@gmail.com',first_name='Jeff',last_name='Brooks',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='buchananr@metro.net', password='buchananr@metro.net',first_name='Riah',last_name='Buchanan',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='burnsb@metro.net', password='burnsb@metro.net',first_name='Barbara',last_name='Burns',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='ACAIN@HRTRANSIT.ORG', password='ACAIN@HRTRANSIT.ORG',first_name='Alesia',last_name='Cain',affiliation='Hampton Roads Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='andrea.campbell@consensusinc.com', password='andrea.campbell@consensusinc.com',first_name='Andrea',last_name='Campbell',affiliation='Consensus Inc.')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jennie.campos@smgov.net', password='jennie.campos@smgov.net',first_name='Jennie',last_name='Campos',affiliation='City of Santa Monica - Big Blue Bus')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='caser@scrra.net', password='caser@scrra.net',first_name='Russell',last_name='Case',affiliation='Metrolink')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Castanonr@metro.net', password='Castanonr@metro.net',first_name='Robert',last_name='Castanon',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Chakladara@scrra.net', password='Chakladara@scrra.net',first_name='Arun',last_name='Chakladar',affiliation='Southern California Regional Rail Authority')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='diana.chang@culvercity.org', password='diana.chang@culvercity.org',first_name='Diana',last_name='Chang',affiliation='City of Culver City / Culver CityBus')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Mark.Chang@ch2m.com', password='Mark.Chang@ch2m.com',first_name='Mark',last_name='Chang',affiliation='CH2M HILL')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dco1+eventbrite@dco1.com', password='dco1+eventbrite@dco1.com',first_name='Danny',last_name='Cohen',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='connors@metro.net', password='connors@metro.net',first_name='Scott',last_name='Connor',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Akima.Cornell@chm2.com', password='Akima.Cornell@chm2.com',first_name='Dr. Akima',last_name='Cornell',affiliation='CH2M HILL')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Autonomous Vehicles', password='Autonomous Vehicles',first_name='Gregory G. Curtin',last_name='Curtin',affiliation=' Ph.D.')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='lrp929@gmail.com', password='lrp929@gmail.com',first_name='Lilia',last_name='Da Silva',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Autonomous Vehicles', password='Autonomous Vehicles',first_name='Frank',last_name='de Windt',affiliation='Aeon Group')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='robert@luxvirtual.com', password='robert@luxvirtual.com',first_name='Robert',last_name='DeCou',affiliation='Lux Virtual')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='mark.denardo@gmail.com', password='mark.denardo@gmail.com',first_name='Mark',last_name='DeNardo',affiliation='Pixeljam')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='holmank@scrra.net', password='holmank@scrra.net',first_name='Michael P.',last_name='DePallo',affiliation='SCRRA/Metrolink')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kari.derderian@lacity.org', password='kari.derderian@lacity.org',first_name='kari',last_name='Derderian',affiliation='LADOT')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kd1@att.com', password='kd1@att.com',first_name='Keith',last_name='Dettloff',affiliation='AT&T')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='joedevon@gmail.com', password='joedevon@gmail.com',first_name='Joe',last_name='Devon',affiliation='DIAMOND')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='downeyj@metro.net', password='downeyj@metro.net',first_name='John',last_name='Downey',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Autonomous Vehicles', password='Autonomous Vehicles',first_name='Brian',last_name='Dunphy',affiliation='Gimbal')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='joyce.edson@lacity.org', password='joyce.edson@lacity.org',first_name='Joyce',last_name='Edson',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kengel@glendaleca.gov', password='kengel@glendaleca.gov',first_name='Kathryn',last_name='Engel',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Autonomous Vehicles', password='Autonomous Vehicles',first_name='Rocco',last_name='Fabiano',affiliation='Gimbal')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='savita@symsoftsolutions.com', password='savita@symsoftsolutions.com',first_name='Savita',last_name='Farooqui',affiliation='SymSoft Solutions')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='pfaust@gardenabus.com', password='pfaust@gardenabus.com',first_name='Paula',last_name='Faust',affiliation='Gardena bus lines')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='David.Figueroa@t-kartorusa.com', password='David.Figueroa@t-kartorusa.com',first_name='David',last_name='Figueroa',affiliation='T-Kartor USA Corp.')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='fogelk@metro.net', password='fogelk@metro.net',first_name='Kali',last_name='Fogel',affiliation='Metro/RIITS')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dfretheim@acireinc.com', password='dfretheim@acireinc.com',first_name='Derek',last_name='Fretheim',affiliation='ACIRE')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='egale@ccala.org', password='egale@ccala.org',first_name='Ezra',last_name='Gale',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='nat.gale@lacity.org', password='nat.gale@lacity.org',first_name='Nat',last_name='Gale',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dexter.galvez@smgov.net', password='dexter.galvez@smgov.net',first_name='Dexter',last_name='Galvez',affiliation='Big Blue Bus')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='bgebha@mtc.ca.gov', password='bgebha@mtc.ca.gov',first_name='Brian',last_name='Gebhardt',affiliation='Metropolitan Transportation Commission')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='owen.gorman@gmail.com', password='owen.gorman@gmail.com',first_name='Owen',last_name='Gorman',affiliation='UCLA Luskin School of Public Policy')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='granatz@metro.net', password='granatz@metro.net',first_name='Zach',last_name='Granat',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='erik.griswold@gmail.com', password='erik.griswold@gmail.com',first_name='Erik',last_name='Griswold',affiliation='Copehnagenize Design Company')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='hamideha@metro.net', password='hamideha@metro.net',first_name='Ashad',last_name='Hamideh',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Next Gen Fares', password='Next Gen Fares',first_name='Alex',last_name='Hammer-Barulich',affiliation='Gladstein')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jhicks@initusa.com', password='jhicks@initusa.com',first_name='Jim',last_name='Hicks',affiliation='INIT Innovations')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='hinesk@metro.net', password='hinesk@metro.net',first_name='Kelly',last_name='Hines',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='mholguin@arellanoassociates.com', password='mholguin@arellanoassociates.com',first_name='Melissa',last_name='Holguin',affiliation='Arellano Associates')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rachel.m.horning@gmail.com', password='rachel.m.horning@gmail.com',first_name='Rachel',last_name='Horning',affiliation='BizFed')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rachel.m.horning@gmail.com', password='rachel.m.horning@gmail.com',first_name='Rachel',last_name='Horning',affiliation='BizFed')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='thuang579@gmail.com', password='thuang579@gmail.com',first_name='Tiffany',last_name='Huang',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='animemanz@gmail.com', password='animemanz@gmail.com',first_name='Erick',last_name='Huerta',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='art.ida@culvercity.org', password='art.ida@culvercity.org',first_name='Art',last_name='Ida',affiliation='Culver CityBus')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='isaacs_e@yahoo.com', password='isaacs_e@yahoo.com',first_name='Eddie',last_name='Isaacs',affiliation='Caltrans')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='ajackson@cityofmontebello.com', password='ajackson@cityofmontebello.com',first_name='Aurora',last_name='Jackson',affiliation='Montebello Bus Lines')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='mikejanusek@gmail.com', password='mikejanusek@gmail.com',first_name='Michael',last_name='Janusek',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='sjavid@aeongroupllc.com', password='sjavid@aeongroupllc.com',first_name='Shirin',last_name='Javid',affiliation='Aeon Group')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Autonomous Vehicles', password='Autonomous Vehicles',first_name='James',last_name='Jeon',affiliation='Gimbal')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jeony@scrra.net', password='jeony@scrra.net',first_name='Yena',last_name='Jeon',affiliation='Metrolink')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jonesre@metro.net', password='jonesre@metro.net',first_name='Reinland',last_name='Jones',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dkaminsky@laworldsfair.org', password='dkaminsky@laworldsfair.org',first_name='Dotty',last_name='Kaminsky',affiliation='Los Angeles World-s Fair')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='tony.kim@kaonsoft.com', password='tony.kim@kaonsoft.com',first_name='Tony',last_name='Kim',affiliation='Kaonsoft/CEO')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='mkroncke@invoketechnologies.com', password='mkroncke@invoketechnologies.com',first_name='Mark',last_name='Kroncke',affiliation='Invoke Tech')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kukreja.charu@gmail.com', password='kukreja.charu@gmail.com',first_name='Charu',last_name='Kukreja',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Josh.Kurpies@asm.ca.gov', password='Josh.Kurpies@asm.ca.gov',first_name='Josh',last_name='Kurpies',affiliation='Office of Assemblymember Richard Bloom')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='joe.lavers@gmail.com', password='joe.lavers@gmail.com',first_name='Joseph',last_name='Lavers',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='law@scag.ca.gov', password='law@scag.ca.gov',first_name='Philip',last_name='Law',affiliation='SCAG')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='brian.k.lee@lacity.org', password='brian.k.lee@lacity.org',first_name='Brian',last_name='Lee',affiliation='LADOT')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='danielee@kaonsoft.com', password='danielee@kaonsoft.com',first_name='Daniel',last_name='Lee',affiliation='Kaonsoft')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='klee@lbtransit.com', password='klee@lbtransit.com',first_name='Kevin',last_name='Lee',affiliation='Long Beach Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='borja.leon@lacity.org', password='borja.leon@lacity.org',first_name='Borja',last_name='Leon',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='libane@metro.net', password='libane@metro.net',first_name='cris',last_name='liban',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dluey@foothilltransit.org', password='dluey@foothilltransit.org',first_name='Donald',last_name='Luey',affiliation='Foothill Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Luuj@metro.net', password='Luuj@metro.net',first_name='Jaclyn',last_name='Luu',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='lancemacniven@gmail.com', password='lancemacniven@gmail.com',first_name='Lance',last_name='MacNiven',affiliation='UCLA')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='hughjohn@civicresource.com', password='hughjohn@civicresource.com',first_name='HughJohn',last_name='Malanaphy',affiliation='Civic Resource Group')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='cassy.jean@gmail.com', password='cassy.jean@gmail.com',first_name='Casaundra',last_name='Mangan',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='bmao@octa.net', password='bmao@octa.net',first_name='Bill',last_name='Mao',affiliation='OCTA')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='mchught@trimet.org', password='mchught@trimet.org',first_name='Tim',last_name='McHugh',affiliation='TriMet')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rich@thecriscomcompany.com', password='rich@thecriscomcompany.com',first_name='Illissa',last_name='Mestas',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='gary.miskell@vta.org', password='gary.miskell@vta.org',first_name='Gary',last_name='Miskell',affiliation='Santa Clara Valley Transportation Authority')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rmisra@bart.gov', password='rmisra@bart.gov',first_name='Ravi',last_name='Misra',affiliation='SF BART')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='ymoaven@latourism.org', password='ymoaven@latourism.org',first_name='Yasmin',last_name='Moaven',affiliation='Los Angeles Tourism Board')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='abhi.nemani@lacity.org', password='abhi.nemani@lacity.org',first_name='Abhi',last_name='Nemani',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='gnord@octa.net', password='gnord@octa.net',first_name='Greg',last_name='Nord',affiliation='OCTA')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='fogrady@usc.edu', password='fogrady@usc.edu',first_name='Fintan',last_name='O-Grady',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='toneill@actransit.org', password='toneill@actransit.org',first_name='Tom',last_name='O-Neill',affiliation='AC Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='daniel.osztreicher@lacity.org', password='daniel.osztreicher@lacity.org',first_name='Daniel',last_name='Osztreicher',affiliation='Office of Councilmember Mike Bonin')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='james.owen@lacity.org', password='james.owen@lacity.org',first_name='James',last_name='Owen',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='alex@phelpstotalmarket.com', password='alex@phelpstotalmarket.com',first_name='Alex',last_name='Perez',affiliation='Phelps Total Market')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='nancy.perlman@lacity.org', password='nancy.perlman@lacity.org',first_name='Nancy',last_name='Perlman',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='curtis@fourninestech.com', password='curtis@fourninestech.com',first_name='Curtis',last_name='Pierce',affiliation='Four Nines Technologies')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='polkj@metro.net', password='polkj@metro.net',first_name='Jamal',last_name='Polk',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='marcel.porras@lacity.org', password='marcel.porras@lacity.org',first_name='Marcel',last_name='Porras',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='prieto@accessla.org', password='prieto@accessla.org',first_name='Ruben',last_name='Prieto',affiliation='Access Services')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='adamrabb@outlook.com', password='adamrabb@outlook.com',first_name='Adam',last_name='Rabb',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jraquel@foothilltransit.org', password='jraquel@foothilltransit.org',first_name='Joseph',last_name='Raquel',affiliation='Foothill Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='arenteria@gardenabus.com', password='arenteria@gardenabus.com',first_name='Adrianna',last_name='Renteria',affiliation='Gardena Municipal Bus Lines')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jared@personal.jaredrimer.net', password='jared@personal.jaredrimer.net',first_name='Jared',last_name='Rimer',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='daniel.rodman@lacity.org', password='daniel.rodman@lacity.org',first_name='Daniel',last_name='Rodman',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rosenberge@gmail.com', password='rosenberge@gmail.com',first_name='Evan',last_name='Rosenberg',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='ssora@earthlink.net', password='ssora@earthlink.net',first_name='Ted',last_name='Ross',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jrothe-kushel@bos.lacounty.gov', password='jrothe-kushel@bos.lacounty.gov',first_name='Jethro',last_name='Rothe-Kushel',affiliation='County of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kati@civicprojects.org', password='kati@civicprojects.org',first_name='Kati',last_name='Rubinyi',affiliation='Civic Projects')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='saponaran@metro.net', password='saponaran@metro.net',first_name='Nick',last_name='Saponara',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='saraviag@metro.net', password='saraviag@metro.net',first_name='Gabriela',last_name='Saravia',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rich@thecriscomcompany.com', password='rich@thecriscomcompany.com',first_name='Rich',last_name='Sarian',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='LeslieRedondoBeach@gmail.com', password='LeslieRedondoBeach@gmail.com',first_name='Leslie',last_name='Scott',affiliation='Redondo Beach')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='varoujs@gmail.com', password='varoujs@gmail.com',first_name='Varouj',last_name='Seuylemezian',affiliation='nTier Solutions')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='shimshona4@gmail.com', password='shimshona4@gmail.com',first_name='Amy',last_name='Shimshon-Santo',affiliation='Claremont Graduate University')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jason@thecriscomcompany.com', password='jason@thecriscomcompany.com',first_name='Jason',last_name='Siegen',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dsmith@lbtransit.com', password='dsmith@lbtransit.com',first_name='Dino',last_name='Smith',affiliation='Long Beach Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='smithe@metro.net', password='smithe@metro.net',first_name='Erin',last_name='Smith',affiliation='LACMTA-ExpressLanes')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Wirless Connectivity', password='Wirless Connectivity',first_name='Randall',last_name='Smith',affiliation='Martin Outdoor Media')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='PATRICKSOTO@EARTHLINK.NET', password='PATRICKSOTO@EARTHLINK.NET',first_name='Patrick',last_name='Soto',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jenstein04@gmail.com', password='jenstein04@gmail.com',first_name='Jen',last_name='Stein',affiliation='SCA | University of Southern California')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jstutes@railLA.org', password='jstutes@railLA.org',first_name='Jeremy',last_name='Stutes',affiliation='railLA')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='suttond@metro.net', password='suttond@metro.net',first_name='David',last_name='Sutton',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='rodd.talebi.intern@lacity.org', password='rodd.talebi.intern@lacity.org',first_name='Rodd',last_name='Talebi',affiliation='City of Los Angeles')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='tshark@gmail.com', password='tshark@gmail.com',first_name='Todd',last_name='Terrazas',affiliation='Brainitch')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='joonie.tolosa@vta.org', password='joonie.tolosa@vta.org',first_name='Joonie',last_name='Tolosa',affiliation='Santa Clara Valley Transportation Authority')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='torresc@metro.net', password='torresc@metro.net',first_name='Carl',last_name='Torres',affiliation='Metro')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='tsuei@accessla.org', password='tsuei@accessla.org',first_name='William',last_name='Tsuei',affiliation='Access Services')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='kturner@torranceCA.gov', password='kturner@torranceCA.gov',first_name='Kim',last_name='Turner',affiliation='Torrance Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='Julie.Vazquez@lacity.org', password='Julie.Vazquez@lacity.org',first_name='Julie',last_name='Vazquez',affiliation='LADOT')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='aveis@lacbos.org', password='aveis@lacbos.org',first_name='Andrew',last_name='Veis',affiliation='L.A. County Supervisor Don Knabe')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dwahi@lbtransit.com', password='dwahi@lbtransit.com',first_name='Dadisi',last_name='Wahi',affiliation='Long Beach Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='dwahi@lbtransit.com', password='dwahi@lbtransit.com',first_name='Dadisi',last_name='Wahi',affiliation='Long Beach Transit')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='donnajw@usc.edu', password='donnajw@usc.edu',first_name='Donnajean',last_name='Ward',affiliation='USC Bedrosian Center')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jweinstein@mtc.ca.gov', password='jweinstein@mtc.ca.gov',first_name='Jason',last_name='Weinstein',affiliation='Metropolitan Transportation Commission')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='wheatonc@scrra.net', password='wheatonc@scrra.net',first_name='Chris',last_name='Wheaton',affiliation='Metrolink')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='twolf@initusa.com', password='twolf@initusa.com',first_name='Thomas',last_name='Wolf',affiliation='INIT Innovation in Transportation Inc.')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='aimee.wyatt@smgov.net', password='aimee.wyatt@smgov.net',first_name='Aimee',last_name='Wyatt',affiliation='City of Santa Monica - Big Blue Bus')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='jennyjingmingyu@gmail.com', password='jennyjingmingyu@gmail.com',first_name='Jenny',last_name='Yu',affiliation='')
UserRoles.create(user=me,role=participant_role)

me=User.create(email='wfzalokar@gmail.com', password='wfzalokar@gmail.com',first_name='William',last_name='Zalokar',affiliation='')
UserRoles.create(user=me,role=participant_role)

