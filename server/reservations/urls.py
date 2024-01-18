from django.urls import path
from . import views

urlpatterns = [
    path('', views.reserve, name='reserve'),
    path('csrf/', views.get_csrf_token, name='get_csrf_token'),
]
