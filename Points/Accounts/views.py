from django.shortcuts import render

# Create your views here.
def home(request):
	return render(request=request,template_name='Accounts/template_name.html', context={'key':'this is my value'})