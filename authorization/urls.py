from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('upload/', views.upload_audio, name='upload_audio'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]