from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cost/', views.cost, name='cost'),
    path('invoice/', views.invoice, name='invoice'),
    path('login/', views.login_view, name='login'),
    path('prosses/', views.prosses, name='prosses'),
    path('submit/', views.submit_cost_estimate, name='submit_cost_estimate'),
    path('auth/check_phone/', views.check_phone, name='check_phone'),
    path('auth/send_email_code/', views.send_verification_email, name='send_verification_email'),
    path('auth/check_email_code/', views.check_verification_email, name='check_verification_email'),
    path('auth/', views.auth_user, name='auth_user'),
path('auth/status/', views.auth_status, name='auth_status'),

]
