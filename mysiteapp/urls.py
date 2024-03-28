from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', views.index),
    path('register/', views.SignUp.as_view()),
    path('login/', LoginView.as_view(template_name='mysiteapp/signup.html'), name='login'),
    path('reset_password/', LoginView.as_view(template_name='mysiteapp/reset_password.html')),
    path('logout/', LogoutView.as_view(template_name='mysiteapp/logout.html')),
]
