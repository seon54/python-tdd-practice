from django.contrib import admin
from django.urls import path
from lists import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('lists/the-only-list-in-the-world/', views.view_list, name='view-list'),
    path('lists/new', views.new_list, name='new-list'),
    path('admin/', admin.site.urls),
]
