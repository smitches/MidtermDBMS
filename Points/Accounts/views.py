from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from datetime import datetime

from .data_gen import main
from .models import PointsUser, PointsOwnedTransaction, PointsToDonateMonthBalance

# Create your views here.
def home(request):
	# call main if you want when you go to localhost:8000/
	# main()
	return render(request=request,template_name='Accounts/template_name.html', context={'key':'this is my home page'})

def about(request):
	# call main if you want when you go to localhost:8000/
	# main()
	return render(request=request,template_name='Accounts/template_name.html', context={'key':'this is my about page'})

class CreateDonation(LoginRequiredMixin, generic.CreateView):
	## TODO: ON SAVE, REDUCE DONATABLE BALANCE
	model = PointsOwnedTransaction
	fields = ['owner','amount_transacted']
	template_name = 'Accounts/create_donation.html' #directory structure in './templates'
	success_url = reverse_lazy('accounts_app:home') #defined in urls.py
	def form_valid(self, form):
		form.instance.donator = self.request.user.pointsuser
		form.instance.date_transacted = datetime.now()
		#TODO: make sure they are donating less than donatable balance. return false if problem.
		return super().form_valid(form)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["donatable_balance"] = self.request.user.pointsuser.get_donatable_balance()
		return context