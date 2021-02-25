from django.urls import path

from . import views

urlpatterns = [
    path('', views.testProcess, name='pptserver answer'),
]
