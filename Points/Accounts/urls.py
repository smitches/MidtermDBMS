from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'accounts_app'

urlpatterns = [
	path('', home, name = 'home'),
	path('donate/', CreateDonation.as_view(), name = 'donate'),
	path('about/', about, name = 'about'),

	path('logout/', auth_views.LogoutView.as_view(
		template_name='Accounts/logout.html'), name='logout'),
	path('login/', auth_views.LoginView.as_view(
		template_name='Accounts/login.html'), name='login'),
	
]