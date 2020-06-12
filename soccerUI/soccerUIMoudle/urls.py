from django.contrib import admin
from django.urls import path, include
from soccerUI.HttpHandlers.HttpHandler import HttpHandler
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


httphandler = HttpHandler()


urlpatterns = [
    path('', include('pages.urls')),
    path('admin/', admin.site.urls),
    path('db/insert/', httphandler.insert_to_db),


]

urlpatterns += staticfiles_urlpatterns()
