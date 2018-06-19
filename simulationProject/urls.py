from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^queens_problem/', include('queensProblem.urls')),
    url(r'^admin/', admin.site.urls),
]
