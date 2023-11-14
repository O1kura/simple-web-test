from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('members/', views.members, name='members'),
    path('members/add',views.add, name='add'),
    path('members/details/<int:id>',views.details,name='details'),
    path('testing/', views.testing, name='testing'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout')
]