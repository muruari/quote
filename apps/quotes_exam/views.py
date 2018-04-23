from __future__ import unicode_literals
import bcrypt, time
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime

def current_user(request):
	return User.objects.get(id = request.session['user_id'])


def registration(request):
	return render(request, 'quotes_exam/registration.html')


def register(request):
    check = User.objects.validate(request.POST)
    if request.method != 'POST':
		return redirect('/')
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="register")
            return redirect('/')

    passwd = request.POST['password']
    if len(check) == 0:
		hashed_pw = bcrypt.hashpw(str(passwd).encode(), bcrypt.gensalt())

    #Creates a new user in the database:
		user = User.objects.create(
			name = request.POST['name'],
			alias = request.POST['alias'],
			email = request.POST['email'],
			password = hashed_pw,
		    date_of_birth = request.POST['date_of_birth']
        )


    email = request.POST['email']
    user = User.objects.get(email = email) # THIS LINE results in JSON serializable error because I was capturing the ENTIRE user object into session.
    request.session['user_id'] = user.id
    request.session['name'] = user.name

    return redirect('/dashboard')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    user = User.objects.filter(email = request.POST.get('email')).first()
    if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        return redirect('/dashboard')
    else: 
        messages.add_message(request, messages.INFO, 'Your credentials are invalid! Please try again.', extra_tags="login")
        return redirect('/')
    return redirect('/dashboard')

	

def logout(request):
		request.session.clear()
		return redirect('/')


def dashboard(request):
	context = {
        'all_quotes' : Quote.objects.exclude(quotes = User.objects.get(id = request.session['user_id'])),
        'my_quotes' : Quote.objects.filter(quotes = User.objects.get(id = request.session['user_id']))

    }
        return render(request, 'quotes_exam/dashboard.html', context)


def create_quote(request):

    #Creates a new quote in the database:

    check = Quote.objects.validate_quote(request.POST)
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="quotes")
            return redirect('/dashboard')


    if len(check) == 0:

        user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.create(
                quote_author = request.POST['quote_author'],
                quote_text = request.POST['quote_text'],
                posted_by = user
            )
        return redirect('/dashboard', quote)


def user_page(request, id):
    user = User.objects.get(id = id)
    context = {
        'user' : user,
        'count' : len(Quote.objects.filter(posted_by = user)),
        'my_quotes' : Quote.objects.filter(posted_by = user)
    }
    return render(request, 'quotes_exam/user.html', context)


def add_quote(request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get(id = id)
    quote.quotes.add(user)
    quote.save()
    return redirect('/dashboard')

def remove_quote(request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get(id = id)
    quote.quotes.remove(user)
    return redirect('/dashboard')
