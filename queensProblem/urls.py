from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ajax/start_simulation/$', views.QueensSimulation, name='QueensSimulation'),
]