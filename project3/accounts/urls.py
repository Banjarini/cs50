from django.urls import include, path
from . import views


urlpatterns = [
    path('Sign_Up/', views.sign_up.as_view(), name='signup'),
    # path('Login/', views.login_view, name='login'),
    path('Password_Reset/', views.reset_password, name='reset_password'),
    path('', include('django.contrib.auth.urls')),
]
