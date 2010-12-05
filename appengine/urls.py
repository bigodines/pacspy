from django.conf.urls.defaults import *

from views import MainView, PacView

urlpatterns = patterns('',
		('^$', MainView), 
		('^pac/$', PacView),
)

# vim: set ts=4 sw=4 et:
