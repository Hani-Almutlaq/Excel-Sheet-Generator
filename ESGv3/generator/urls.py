from django.urls import path
from .views import index, generate, end

urlpatterns = [
    path("", index, name="index"),
    path('generate/', generate, name='generate'),
    path("end/", end, name="end"),
]
