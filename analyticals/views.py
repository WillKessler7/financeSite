from django.http import HttpResponse
from django.views import View
from django.shortcuts import render
from django.template import loader
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Stock, PortEntries

class loginView(View):

    def get(self, request):

        template = loader.get_template('analyticals/loginView.html')
        context = {}
        return HttpResponse(template.render(context, request))

class stockPickView(View):
    def post(self, request):
        
        # if the username imported from template's form is for logging in,
        if 'inputedUsername' in request.POST.keys():

            # try to authenticate the inputed username and password
            username = request.POST['inputedUsername']
            password = request.POST['inputedPassword']
            user = authenticate(username=username, password=password)

            # if the user was found (authenticated),
            if user is not None:
                # login the user
                login(request, user)
                # set loggedIn variable to True for use in templates
                loggedIn = True

            else:
                loggedIn = False
                password = request.POST['inputedPassword']
                # display password as an HttpResponse as a test case
                return HttpResponse(password)

        # otherwise, if the user was not found,
        else:
            # not for login, will deal with making accounts and logouts later
            pass
        #else:
            #logout(request)

        # save the variables of whether the user is loggedin and the username
        # to the correct template
        context = {
            'loggedIn': loggedIn,
            'username': username
        }

        # assign template to be loaded to the correct view
        template = loader.get_template('analyticals/stockPickView.html')

        return HttpResponse(template.render(context, request))


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
