from django.conf.urls.defaults import *
from django.contrib.auth.views import logout
from django.contrib import admin

admin.autodiscover()
from django.conf import settings

from EAV_Model.views import *
from EAV_Model.models import *


urlpatterns= patterns('', url(r'^login/', login_user), url(r'^patient/', Patient_View))

#This definition creates a url for all the studies in the database
for study in Study.objects.all():
	studyName = str(study).split(" ")
	path = url(r'^'+str(studyName[0])+'/main/', Main_View)
	urlpatterns.append(path) 	
	for stage in Stage.objects.filter(studyId=study):
		stageName = str(stage).split(" ")
		path = url(r'^'+studyName[0]+'/'+str(stageName[1])+'/', Form_View)
		urlpatterns.append(path) 