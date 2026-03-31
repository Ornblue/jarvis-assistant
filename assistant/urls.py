from django.urls import path
from .views import home, process_command

urlpatterns = [
    path('', home),
    path('api/process/', process_command),
]