#from django.conf.urls import patterns,include,url
from django.conf.urls import include, url
from django.contrib import admin
 
from oltp_admin import views
admin.autodiscover()

urlpatterns = (
	url(r'^$',views.index,name='index'),
	url(r'^login/',views.login,name='login'),
	url(r'^logout/',views.logout,name='logout'),
	url(r'^register/',views.register,name='register'),
	url(r'^admin/review/',views.review,name='review'),
	url(r'^admin/',views.admin,name='admin'),

)

