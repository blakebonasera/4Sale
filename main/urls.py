from django.urls import path     
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('dashboard', views.success),
    path('logout', views.logout),
    path('login', views.login),
    path('addlisting', views.addListing),
    path('newlisting', views.listing),
    path('view/<int:num>', views.viewListing)
]