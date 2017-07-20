#from django.conf.urls import patterns,include,url
from django.conf.urls import include, url
from django.contrib import admin
 
from QaPlat import views
admin.autodiscover()

urlpatterns = (
	url(r'^index/$',views.index,name='index'),
	url(r'^uploadFile/$',views.uploadFile,name='uploadFile'),
	url(r'^qaPlat/$',views.qaPlat,name='qaPlat'),
	url(r'^like/$',views.likeService,name='likeService'),
	url(r'^publicQ/$',views.publicQ,name='publicQ'),
	url(r'^oneQuestion/',views.oneQuestion,name='oneQuestion'),
	url(r'^oneQuestion/\d+?/',views.oneQuestion,name='oneQuestion'),
	url(r'^commentSubmit/$',views.commentSubmit,name='commentSubmit'),
	url(r'^message/$',views.message,name='message'),
	url(r'^profile/$',views.profile,name='profile'),
	url(r'^followS/$',views.followS,name='followS'),
	url(r'^unfollowS/$',views.unfollowS,name='unfollowS'),
	url(r'^person/own/$',views.own,name='own'),
	url(r'^person/.*?/$',views.person,name='person'),

)

