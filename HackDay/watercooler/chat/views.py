from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def create_user(username, email, password):
	new_user = User.objects.create_user(username, email, password)
	new_user.save()

@csrf_exempt
def login_user(request):
	if not request.method == 'POST':
		return render_to_response('login.html')
	else:
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		print username
		print password
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return render_to_response('found.html')
		# else:
		# 	# Return a 'disabled account' error message
	# else:
	# 	# Return an 'invalid login' error message.

def logout_user(request):
	logout(request)

def chat_view(request):
	if not request.user.is_authenticated():
		return render_to_response('login.html')
		# return redirect('/login/')
	else:
		return render_to_response('chat.html')