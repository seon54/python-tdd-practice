from django.contrib import admin
from django.urls import path, include
from lists import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/', include('lists.urls')),
    path('admin/', admin.site.urls),
]
