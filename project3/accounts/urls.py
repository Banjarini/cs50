from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name='password_change_form.html',success_url = '/'), name='change_password'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html',success_url = '/accounts/password_reset/done/'), name='reset_password'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')),
    path('reset/<uidb64>/<token>/',     auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),     name='password_reset_confirm'),
    path('reset/done/',     auth_views.PasswordResetCompleteView.as_view(),     name='password_reset_complete'),
    path('', include('django.contrib.auth.urls')),
]
