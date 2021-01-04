from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='AcaLoc-home'),
    path('about/', views.about, name='AcaLoc-about'),
    path('deneme/',views.deneme,name = 'AcaLoc-deneme'),
]