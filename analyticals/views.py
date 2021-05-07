from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Stock, PortEntries

class loginView(View):
    def post(self, request):
        # sets loggedIn var to False as default because user begins not
        # logged in
        loggedIn = False

        # try to authenticate the inputed username and password
        username = request.POST['inputedUsername']
        password = request.POST['inputedPassword']

        # save the variables of whether the user is loggedin and the username
        # to the correct template
        context = {
            'loggedIn': loggedIn,
            'username': username
        }

        # if the username imported from template's form is for logging in,
        if 'inputedUsername' in request.POST.keys():

            user = authenticate(username=username, password=password)

            # if the user was found,
            if user is not None:
                # login the user
                login(request, user)
                # set loggedIn var to true
                loggedIn = True
                # assign template to be loaded to the correct view
                template = loader.get_template('analyticals/stockPickView.html')




            # otherwise, if the user was not found,
            else:
                # loads back to the loginView template
                template = loader.get_template('analyticals/loginView.html')

        # if the form submitted is not for logging in,
        else:
            # don't need to set loggedIn var to false because it is already false
            # pass because I have not written the logout function yet
            pass
            #logout(request)

        return HttpResponse(template.render(context, request))


    def get(self, request):

        template = loader.get_template('analyticals/loginView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockPickView(View):
    def post(self, request):
        # checks if the form submission was for logging out
        if 'logoutButton' in request.POST.keys():
            # redirect to login view
            return redirect("loginView")

        else:
            # will work on the other case later
            pass

    def get(self, request):
        template = loader.get_template('analyticals/stockPickView.html')
        allStocks = Stock.objects.all()
        context = {'allStocks': allStocks }
        print(request.POST)
        return HttpResponse(template.render(context, request))

class graphDisplayView(View):
    def get(self, request):
        template = loader.get_template('analyticals/graphDisplayView.html')
        # put data in context for each view
        context = {}
        return HttpResponse(template.render(context, request))
