from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='guess-home'),
    path('about/', views.about, name='guess-about'),
    path('submit/', views.submit, name='guess-submit'),
    path('submit_one/', views.submit_one, name='guess-submit_one'),

]
###
