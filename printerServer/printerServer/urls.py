from django.conf.urls import url
from django.contrib import admin
from printer import views

urlpatterns = [
    url(r'^printData', views.print_something),
    url(r'^admin/', admin.site.urls),
]
