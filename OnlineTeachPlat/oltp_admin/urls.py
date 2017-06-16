#from django.conf.urls import patterns,include,url
from django.conf.urls import include, url
from django.contrib import admin
 
from oltp_admin import views
admin.autodiscover()

urlpatterns = (
	url(r'^$',views.index,name='index'),
)

