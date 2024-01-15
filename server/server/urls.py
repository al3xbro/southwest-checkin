from django.urls import include, path

urlpatterns = [
    path('reserve/', include('reservations.urls')),
]
