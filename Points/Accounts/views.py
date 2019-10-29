from django.shortcuts import render
from .data_gen import main
# Create your views here.
def home(request):
	# call main if you want when you go to localhost:8000/
	# main()
	return render(request=request,template_name='Accounts/template_name.html', context={'key':'this is my value'})