#from django.conf.urls import patterns,include,url
from django.conf.urls import include, url
from django.contrib import admin
 
from QaPlat import views
admin.autodiscover()

urlpatterns = (
	url(r'^index/',views.index,name='index'),
	url(r'^uploadFile/',views.uploadFile,name='uploadFile'),
	url(r'^qaPlat/',views.qaPlat,name='qaPlat'),
	url(r'^publicQ/',views.publicQ,name='publicQ'),
)

