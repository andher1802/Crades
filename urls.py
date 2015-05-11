from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^(\w+-{0,1}\w*.html)$', 'views.general_templates'),
    url(r'^$', 'views.general_templates',{'page':'index.html'}),
	url(r'^eav/', include('EAV_Model.urls')),
)