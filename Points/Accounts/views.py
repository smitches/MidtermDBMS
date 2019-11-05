from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

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

def admin_dashboard(request):
	context = {'date_ending':PointsToDonateMonthBalance.objects.order_by('-date_expire').first().date_expire}
	context['month_ended']=request.GET.get('month_ended')
	return render(request=request,template_name='Accounts/dashboard.html', context=context)

def end_month(request):
	##TODO:reset month and create new points
	PointsToDonateMonthBalance.objects.order_by('-date_expire')
	print('ended month')
	return redirect(reverse('accounts_app:dashboard')+'?month_ended=True')

class CreateDonation(LoginRequiredMixin, generic.CreateView):
	
	model = PointsOwnedTransaction
	fields = ['owner','amount_transacted']
	template_name = 'Accounts/create_donation.html' #directory structure in './templates'
	success_url = reverse_lazy('accounts_app:thanks') #defined in urls.py

	def form_valid(self, form):

		form.instance.donator = self.request.user.pointsuser
		form.instance.date_transacted = datetime.now()

		##check for errors in form input
		if form.instance.amount_transacted > self.request.user.pointsuser.get_donatable_balance():
			form.add_error(field='amount_transacted',error="You cannot donate more than your donatable balance")
		if form.instance.amount_transacted < 1:
			form.add_error(field='amount_transacted',error="You must donate more than 0 points")
		if form.instance.donator == form.instance.owner:
			form.add_error(field='owner',error="You cannot donate to yourself")
		if form.errors:
			return super().form_invalid(form)

		## There are no errors. Decrease their donatable balance.
		donatebalance = user.pointstodonatemonthbalance_set.filter(date_expire__gte = datetime.now(), date_begin__lte=datetime.now()).first()
		donatebalance.points_remaining -= amount
		donatebalance.save()

		#continue to save donation in pointsownedtransaction
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["donatable_balance"] = self.request.user.pointsuser.get_donatable_balance()
		return context