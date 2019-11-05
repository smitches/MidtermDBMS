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
	return render(request=request,template_name='Accounts/home.html', context={'key':'this is my home page'})

def about(request):
	return render(request=request,template_name='Accounts/about.html', context={'key':'this is my about page'})

def thanks(request):
	return render(request=request,template_name='Accounts/thanks.html')


class CreateDonation(LoginRequiredMixin, generic.CreateView):
	## TODO: ON SAVE, REDUCE DONATABLE BALANCE
	model = PointsOwnedTransaction
	fields = ['owner','amount_transacted']
	template_name = 'Accounts/create_donation.html' #directory structure in './templates'
	success_url = reverse_lazy('accounts_app:thanks') #defined in urls.py
	def form_valid(self, form):
		form.instance.donator = self.request.user.pointsuser
		form.instance.date_transacted = datetime.now()
		if form.instance.amount_transacted > self.request.user.pointsuser.get_donatable_balance():
			form.add_error(field='amount_transacted',error="You cannot donate more than your donatable balance")
		if form.instance.amount_transacted < 1:
			form.add_error(field='amount_transacted',error="You must donate more than 0 points")
		if form.instance.donator == form.instance.owner:
			form.add_error(field='owner',error="You cannot donate to yourself")
		if form.errors:
			return super().form_invalid(form)
		return super().form_valid(form)
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["donatable_balance"] = self.request.user.pointsuser.get_donatable_balance()
		return context