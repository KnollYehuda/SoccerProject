from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('research/', views.research, name='research'),
    # path('/aboutUs/', views.aboutUs, name="aboutUs"),
    path('blog/', views.blog, name="blog"),
    path('contact/', views.contact, name="contact"),
    path('elements/', views.elements, name="elements"),
    path('portfolio/', views.portfolio, name="portfolio"),
    path('services/', views.services, name="services"),

]